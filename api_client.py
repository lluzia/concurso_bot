import requests
from config import API_URL

def fetch_concursos():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            print("[API ERROR] Resposta não é JSON válido")
            return []

    except Exception as e:
        print(f"[API ERROR] {e}")
        return []

