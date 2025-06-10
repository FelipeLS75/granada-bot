FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
# Ajouter ces deux lignes
RUN playwright install
RUN playwright install-deps

EXPOSE 10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "granada_bot:app"]
