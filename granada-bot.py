# app.py
from flask import Flask, request, jsonify
import threading
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time

app = Flask(__name__)

def automate_granada_requests():
    print("▶️ Début du script Playwright...")

    url_login = "https://alojamiento.ugr.es/user/login"
    base_listing_url = "https://alojamiento.ugr.es/alojamientos/pisos-habitaciones"
    username = "LE SOUDER PHILIPPE"
    password = "Plesouder@75"
    message = """Hola, les escribí en 2024. Solo quería saber si tienen algo disponible para 1 mes en julio o agosto (fechas flexibles). Gracias.
–
Hi, I contacted you in 2024. Just checking back this year to see if you might have an apartment available for 1 month in July or August (flexible dates). Thanks."""

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url_login)
            page.fill("#edit-name", username)
            page.fill("#edit-pass", password)
            page.click("input[type='submit'][value='Iniciar sesión']", force=True)
            page.wait_for_load_state("networkidle")
            print("✅ Connecté avec succès")

            current_page = 1
            max_pages = 10

            while current_page <= max_pages:
                print(f"🔎 Page {current_page} en cours...")
                page.goto(f"{base_listing_url}?page={current_page - 1}")
                page.wait_for_load_state("networkidle")

                annonces_hrefs = page.eval_on_selector_all(
                    "a[href*='/alojamientos/pisos-habitaciones/habitacion-']",
                    "elements => elements.map(el => el.href)"
                )

                if not annonces_hrefs:
                    print("❌ Aucune annonce trouvée.")
                    break

                for href in annonces_hrefs:
                    print(f"➡️ Traitement : {href}")
                    page.goto(href)
                    page.wait_for_load_state("networkidle")

                    try:
                        btn = page.wait_for_selector(
                            "a:has-text('Solicitar información'), button:has-text('Solicitar información')", timeout=5000
                        )
                        btn.click()
                        page.wait_for_load_state("networkidle")

                        try:
                            frame = page.frame_locator("iframe.cke_wysiwyg_frame")
                            frame.locator("body.cke_editable").fill(message)
                        except:
                            page.fill("textarea#edit-comentarios, textarea[name='comentarios']", message)

                        page.click('input[type="submit"][value="Guardar"]', force=True)
                        page.wait_for_load_state("networkidle")
                        print("✅ Message envoyé.")
                        time.sleep(1)

                    except PlaywrightTimeoutError:
                        print("⏱️ Bouton 'Solicitar información' introuvable.")
                    except Exception as e:
                        print(f"⚠️ Erreur sur l'annonce : {e}")

                try:
                    next_btn = page.wait_for_selector("a[title='Siguiente página'], a:has-text('Siguiente ›')", timeout=5000)
                    if next_btn and "disabled" not in (next_btn.get_attribute("class") or ""):
                        next_btn.click()
                        page.wait_for_load_state("networkidle")
                        current_page += 1
                    else:
                        break
                except:
                    break

            browser.close()
            print("🛑 Script terminé.")

    except Exception as e:
        print(f"❌ Erreur globale Playwright : {e}")


@app.route('/run-script', methods=['POST'])
def run_script():
    threading.Thread(target=automate_granada_requests).start()
    return jsonify({"status": "Script lancé"}), 200

@app.route('/', methods=['GET'])
def index():
    return "Granada bot is alive", 200
