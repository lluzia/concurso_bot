import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

API_URL = "https://concursos-api.deno.dev"

URL = "https://www.pciconcursos.com.br/"

# filtros opcionais
KEYWORDS = ["prefeitura", "polícia", "tribunal", "TI", "analista", "INSS", "banco", 'câmara']

# regiões desejadas
REGIONS = ["SUDESTE", "SUL", "CENTRO-OESTE", "NORDESTE"]
# REGIONS = ["CENTRO-OESTE"]
REGION_UFS = {
    "NORTE": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
    "NORDESTE": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "CENTRO-OESTE": ["DF", "GO", "MT", "MS"],
    "SUDESTE": ["ES", "MG", "RJ", "SP"],
    "SUL": ["PR", "RS", "SC"],
}

def get_allowed_ufs():
    ufs = set()

    for region in REGIONS:
        if region in REGION_UFS:
            ufs.update(REGION_UFS[region])

    return list(ufs)


UF_FILTER = get_allowed_ufs()
