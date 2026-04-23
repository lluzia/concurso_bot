import requests
from bs4 import BeautifulSoup
from config import KEYWORDS, URL
import time

URL = URL

def fetch_with_retry(url, retries=3):
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response.text

            print(f"[WARN] Tentativa {attempt+1} falhou: {response.status_code}")

        except Exception as e:
            print(f"[ERROR] Tentativa {attempt+1}: {e}")

        time.sleep(2)

    return None


def scrape_pci():
    concursos = []

    html = fetch_with_retry(URL)

    if not html:
        print("[ERROR] Falha ao acessar PCI após retries")
        return []

    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a")

    for a in links:
        titulo = a.get_text(strip=True)
        link = a.get("href")

        if not titulo or not link:
            continue

        if "concurso" not in titulo.lower():
            continue

        if len(titulo) < 25:
            continue

        if KEYWORDS and not any(k in titulo.lower() for k in KEYWORDS):
            continue

        if not link.startswith("http"):
            link = f"https://www.pciconcursos.com.br{link}"

        concursos.append({
            "titulo": titulo,
            "link": link,
            "id": link
        })

    print(f"[INFO] PCI encontrados: {len(concursos)}")
    return concursos