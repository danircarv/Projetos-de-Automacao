import os
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(name: str, required=True, default=None):
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"A variável de ambiente '{name}' é obrigatória e não foi encontrada.")
    return value


EMAIL_USER = get_env_variable("EMAIL_USER")
EMAIL_PASS = get_env_variable("EMAIL_PASS")
EMAIL_SMTP = get_env_variable("EMAIL_SMTP", default="smtp.gmail.com")
EMAIL_PORT = int(get_env_variable("EMAIL_PORT", default=587))


PRODUCTS_RAW = get_env_variable("PRODUCTS")

# Converte a string PRODUCTS em lista de dicionários
# Formato interno: [{"name": ..., "url": ..., "target": ...}, ...]
PRODUCTS = []
for item in PRODUCTS_RAW.split(","):
    try:
        name, url, target_price = item.strip().split("|")
        PRODUCTS.append({
            "name": name.strip(),
            "url": url.strip(),
            "target_price": float(target_price.strip())
        })
    except ValueError:
        raise ValueError(f"Formato inválido em PRODUCTS: '{item}'. Use Nome|URL|Preço.")


HISTORY_CSV = get_env_variable("HISTORY_CSV", default="data/history.csv")
LOG_FILE = get_env_variable("LOG_FILE", default="logs/price_monitor.log")