import streamlit as st
from scraper_pci import scrape_pci
from config import REGION_UFS
import re
from collections import defaultdict

st.set_page_config(
    page_title="Concursos Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# STYLE
# -------------------------
st.markdown("""
<style>
.card {
    background: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: white;
    border: 1px solid #2c2f36;
}

.highlight-salary {
    border: 1px solid #2ecc71;
}

.highlight-federal {
    border: 1px solid #f1c40f;
}

.badge {
    background: #333;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 12px;
    margin-right: 5px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HELPERS
# -------------------------
def extract_uf(titulo):
    match = re.search(r"-\s*([A-Z]{2})\b", titulo)
    return match.group(1) if match else "??"

def get_region(uf):
    for region, ufs in REGION_UFS.items():
        if uf in ufs:
            return region
    return "OUTROS"

def group_by_region(concursos):
    grouped = defaultdict(list)

    for c in concursos:
        uf = extract_uf(c["titulo"])
        region = get_region(uf)
        c["uf"] = uf
        grouped[region].append(c)

    return grouped

# -------------------------
# 💰 DETECT SALARY
# -------------------------
def extract_salary(text):
    matches = re.findall(r"R\$\s?([\d\.,]+)", text)

    values = []
    for m in matches:
        num = m.replace(".", "").replace(",", ".")
        try:
            values.append(float(num))
        except:
            pass

    return max(values) if values else 0

def is_high_salary(text, threshold=5000):
    return extract_salary(text) >= threshold

# -------------------------
# 🏛️ DETECT FEDERAL
# -------------------------
FEDERAL_KEYWORDS = [
    "federal", "união", "ministerio", "ministério",
    "ibge", "inss", "receita federal", "pf", "prf"
]

def is_federal(text):
    text = text.lower()
    return any(k in text for k in FEDERAL_KEYWORDS)

# -------------------------
# CACHE
# -------------------------
@st.cache_data(ttl=3600)
def get_data():
    return scrape_pci()

# -------------------------
# HEADER
# -------------------------
st.title("📢 Concursos Públicos")

if st.button("🔄 Atualizar dados"):
    st.cache_data.clear()
    st.rerun()

concursos = get_data()

if not concursos:
    st.warning("Nenhum concurso encontrado.")
    st.stop()

# -------------------------
# FILTROS
# -------------------------
ufs = sorted(set(extract_uf(c["titulo"]) for c in concursos))

selected_ufs = st.multiselect(
    "Filtrar por estado",
    options=ufs,
    default=ufs
)

# -------------------------
# PROCESSAMENTO
# -------------------------
filtered = []
high_salary_count = 0
federal_count = 0

for c in concursos:
    uf = extract_uf(c["titulo"])

    if uf not in selected_ufs:
        continue

    salary_flag = is_high_salary(c["titulo"])
    federal_flag = is_federal(c["titulo"])

    if salary_flag:
        high_salary_count += 1

    if federal_flag:
        federal_count += 1

    c["uf"] = uf
    c["high_salary"] = salary_flag
    c["federal"] = federal_flag

    filtered.append(c)

grouped = group_by_region(filtered)

# -------------------------
# METRICS
# -------------------------
m1, m2, m3 = st.columns(3)

m1.metric("Total", len(filtered))
m2.metric("💰 Altos salários", high_salary_count)
m3.metric("🏛️ Federais", federal_count)

# -------------------------
# LISTAGEM
# -------------------------
for region in sorted(grouped.keys()):
    st.markdown(f"### 📍 {region}")

    items = sorted(grouped[region], key=lambda x: x["uf"])

    for c in items:
        classes = "card"

        if c["high_salary"]:
            classes += " highlight-salary"

        if c["federal"]:
            classes += " highlight-federal"

        badges = f"<span class='badge'>{c['uf']}</span>"

        if c["high_salary"]:
            badges += "<span class='badge'>💰 Alto salário</span>"

        if c["federal"]:
            badges += "<span class='badge'>🏛️ Federal</span>"

        st.markdown(f"""
        <div class="{classes}">
            {badges}<br>
            {c['titulo']}<br>
            <a href="{c['link']}" target="_blank">Ver edital →</a>
        </div>
        """, unsafe_allow_html=True)