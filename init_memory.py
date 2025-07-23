import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL_BASE = "https://tophotfashion.x.yupoo.com/albums?tab=gallery"
FICHIER_MEMOIRE = "memory.json"
NB_PAGES = 44
DELAI_CHARGEMENT = 3  # Secondes d’attente entre chaque page

def initialiser_driver():
    options = Options()
    options.add_argument("--headless")  # Mode invisible
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    return driver

def extraire_liens_album(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, "a.album__main")
    return [el.get_attribute("href") for el in elements if el.get_attribute("href")]

def main():
    print("🚀 Initialisation de la mémoire en cours...\n")
    driver = initialiser_driver()
    tous_les_albums = set()

    for page in range(1, NB_PAGES + 1):
        url_page = f"{URL_BASE}&page={page}"
        driver.get(url_page)
        time.sleep(DELAI_CHARGEMENT)

        liens = extraire_liens_album(driver)
        tous_les_albums.update(liens)

        print(f"🔎 Page {page}/{NB_PAGES} → {len(liens)} albums détectés")

    driver.quit()

    with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as f:
        json.dump(sorted(tous_les_albums), f, indent=2, ensure_ascii=False)

    print(f"\n✅ Mémoire initiale créée avec {len(tous_les_albums)} albums.\n")

if __name__ == "__main__":
    main()
