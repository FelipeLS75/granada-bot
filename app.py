from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

def automate_granada_requests():
    print("▶️ Simulation Playwright : envoi message Granada")
    time.sleep(2)
    print("✅ Script terminé.")

@app.route('/run-script', methods=['POST'])
def run_script():
    threading.Thread(target=automate_granada_requests).start()
    return jsonify({"status": "Script lancé"}), 200

@app.route('/', methods=['GET'])
def index():
    return "Granada bot is alive", 200
