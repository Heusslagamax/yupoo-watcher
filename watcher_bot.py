# watcher_bot.py

import os
import json
import time
import subprocess
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import Bot
from datetime import datetime

# Load secrets
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔁 Lancer le scraper_daily.py automatiquement
print("🚀 Lancement du scraper_daily.py...")
subprocess.run(["python", "scraper_daily.py"])

# 🔍 Charger les nouveautés
with open("nouveautes.json", "r") as f:
    nouveautes = json.load(f)

if not nouveautes:
    # 📭 Pas de nouveautés → message simple
    now = datetime.now().strftime("%d/%m/%Y")
    message = f"📭 Aucune nouveauté aujourd’hui ({now}) les gars. À demain !"
    Bot(token=TOKEN).send_message(chat_id=CHAT_ID, text=message)
    print("✅ Aucun nouvel album détecté.")
    exit()

# 🔄 Sinon → envoyer chaque nouveauté avec image
print(f"🆕 {len(nouveautes)} nouveautés détectées. Envoi en cours...")

bot = Bot(token=TOKEN)

# Config Chrome headless
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=options)

for url in nouveautes:
    try:
        driver.get(url)
        time.sleep(2)
        image = driver.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

        # Envoyer sur Telegram
        bot.send_photo(chat_id=CHAT_ID, photo=image, caption=f"🆕 Nouvel album : {url}")
        print(f"✅ Envoyé : {url}")

    except Exception as e:
        print(f"⚠️ Erreur pour {url} : {e}")

driver.quit()

# 🧠 Mettre à jour la mémoire
with open("memory.json", "r") as f:
    memory = set(json.load(f))

memory.update(nouveautes)

with open("memory.json", "w") as f:
    json.dump(sorted(memory), f, indent=2)

# 🧹 Vider le fichier nouveautes
with open("nouveautes.json", "w") as f:
    json.dump([], f)

print("🎉 Toutes les nouveautés ont été envoyées et la mémoire est mise à jour.")
