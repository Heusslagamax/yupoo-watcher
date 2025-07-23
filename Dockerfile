FROM python:3.11-slim

# Installer les dépendances système pour Selenium (headless Chrome)
RUN apt-get update && apt-get install -y \
    wget unzip gnupg curl xvfb libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libasound2 libxtst6 libxrandr2 \
    && apt-get clean

# Installer Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb

# Installer chromedriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Créer l'environnement de travail
WORKDIR /app

# Copier les fichiers
COPY . .

# Installer les packages Python
RUN pip install --no-cache-dir -r requirements.txt

# Lancer le bot
CMD ["python", "watcher_bot.py"]
