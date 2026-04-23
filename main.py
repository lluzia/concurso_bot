from scraper_pci import scrape_pci
from email_sender import send_email
from storage import load_seen, save_seen
from config import UF_FILTER
import re
import smtplib
from email.mime.text import MIMEText
from config import EMAIL_FROM, EMAIL_TO, EMAIL_PASSWORD

def extract_uf(titulo):
    """
    Extrai UF (SP, MG, etc.) do título
    """
    match = re.search(r"\b([A-Z]{2})\b", titulo)
    return match.group(1) if match else None


def main():
    print("[INFO] Iniciando coleta...")

    seen = load_seen()
    print(f"[INFO] Já vistos: {len(seen)}")

    concursos = scrape_pci()

    if not concursos:
        print("[WARN] Nenhum dado coletado.")
        send_alert_error("Bot executou mas não encontrou concursos.")
        return


    print(f"[INFO] Total coletado: {len(concursos)}")

    novos = []

    for c in concursos:
        if c["id"] in seen:
            continue

        uf = extract_uf(c["titulo"])

        # 🔥 FILTRO POR ESTADO
        if UF_FILTER:
            if not uf or uf not in UF_FILTER:
                continue

        novos.append(c)
        seen.add(c["id"])

    if novos:
        print(f"[INFO] {len(novos)} novos concursos encontrados\n")

        for c in novos:
            print(f"- {c['titulo']}")

        send_email(novos)
    else:
        print("[INFO] Nenhum concurso novo (após filtro)")

    save_seen(seen)

def extract_uf(titulo):
    import re

    # padrão mais confiável: "- SP"
    match = re.search(r"-\s*([A-Z]{2})\b", titulo)
    return match.group(1) if match else None

def send_alert_error(message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = "❌ Bot Concursos - Erro detectado"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        print(f"[ALERT ERROR] {e}")

if __name__ == "__main__":
    main()