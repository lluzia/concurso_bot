import smtplib
from email.mime.text import MIMEText
from config import EMAIL_FROM, EMAIL_TO, EMAIL_PASSWORD, REGION_UFS
import re


def extract_uf(titulo):
    match = re.search(r"-\s*([A-Z]{2})\b", titulo)
    return match.group(1) if match else "??"


def get_region(uf):
    for region, ufs in REGION_UFS.items():
        if uf in ufs:
            return region
    return "OUTROS"


def group_concursos(concursos):
    grouped = {}

    for c in concursos:
        uf = extract_uf(c["titulo"])
        region = get_region(uf)

        if region not in grouped:
            grouped[region] = []

        c["uf"] = uf
        grouped[region].append(c)

    return grouped


def generate_html(concursos):
    grouped = group_concursos(concursos)

    html_sections = ""

    for region in sorted(grouped.keys()):
        items = grouped[region]

        # ordena por UF
        items.sort(key=lambda x: x["uf"])

        list_items = ""

        for c in items:
            list_items += f"""
            <li style="margin-bottom:8px;">
                <strong>[{c['uf']}]</strong>
                <a href="{c['link']}" target="_blank" style="text-decoration:none; color:#1a73e8;">
                    {c['titulo']}
                </a>
            </li>
            """

        html_sections += f"""
        <h3 style="margin-top:20px;">📍 {region}</h3>
        <ul style="padding-left:20px;">
            {list_items}
        </ul>
        """

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height:1.6;">
            <h2>📢 Novos Concursos Encontrados</h2>
            <p>Total: {len(concursos)}</p>

            {html_sections}

            <hr>
            <p style="font-size:12px;color:gray;">
                Gerado automaticamente pelo seu bot 🤖
            </p>
        </body>
    </html>
    """

    return html


def send_email(concursos):
    if not concursos:
        return

    if not EMAIL_FROM or not EMAIL_TO or not EMAIL_PASSWORD:
        print("[ERROR] Credenciais de email não configuradas.")
        return

    html_content = generate_html(concursos)

    msg = MIMEText(html_content, "html")
    msg["Subject"] = f"{len(concursos)} novos concursos encontrados"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
            print("[INFO] Email HTML enviado com sucesso!")

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")