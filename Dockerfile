FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

# Set working directory
WORKDIR /app

# Copy your app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Render uses port 10000 by default for web services)
EXPOSE 10000

# Start the app
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "granada_bot:app"]

