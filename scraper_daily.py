import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Configuration
URL_BASE = "https://tophotfashion.x.yupoo.com/albums?tab=gallery"
FICHIER_MEMOIRE = "memory.json"
FICHIER_NOUVEAUTES = "nouveautes.json"
DELAI_CHARGEMENT = 3


def charger_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def enregistrer_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def initialiser_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    return webdriver.Chrome(options=options)


def recuperer_tous_les_albums():
    driver = initialiser_driver()
    driver.get(URL_BASE)
    time.sleep(DELAI_CHARGEMENT)
    albums_urls = set()

    while True:
        elements = driver.find_elements(By.CSS_SELECTOR, 'a.album__main')
        for el in elements:
            url = el.get_attribute('href')
            if url:
                albums_urls.add(url)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')
            if 'disabled' in next_button.get_attribute('class'):
                break
            else:
                next_button.click()
                time.sleep(DELAI_CHARGEMENT)
        except:
            break

    driver.quit()
    return list(albums_urls)


def comparer_et_enregistrer():
    print("\n🚀 Scraping quotidien en cours...")

    anciens_albums = set(charger_json(FICHIER_MEMOIRE))
    tous_albums = set(recuperer_tous_les_albums())
    
    nouveaux = list(tous_albums - anciens_albums)

    if nouveaux:
        print(f"✅ {len(nouveaux)} nouveaux albums détectés.")
        enregistrer_json(FICHIER_NOUVEAUTES, nouveaux)
        enregistrer_json(FICHIER_MEMOIRE, list(tous_albums))
    else:
        print("📭 Aucune nouveauté détectée aujourd'hui.")
        enregistrer_json(FICHIER_NOUVEAUTES, [])
        enregistrer_json(FICHIER_MEMOIRE, list(tous_albums))


if __name__ == '__main__':
    comparer_et_enregistrer()
