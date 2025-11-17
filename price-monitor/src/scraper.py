import requests
from utils import logger, extract_price_from_html, parse_price
from config import PRODUCTS, get_env_variable


# Cabeçalhos para simular navegador
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_html(url, headers=HEADERS):
    """
    Faz requisição GET e retorna HTML bruto.
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info(f"HTML obtido: {url}")
        return response.text
    except requests.RequestException as e:
        logger.error(f"Erro ao obter HTML de {url}: {e}")
        return None



from bs4 import BeautifulSoup

def extract_amazon_price(html):

    soup = BeautifulSoup(html, "html.parser")

    whole = soup.select_one(".a-price-whole")
    fraction = soup.select_one(".a-price-fraction")

    if not whole:
        return None  # deixa fallback tentar

    # Alguns preços vêm com "." dentro (milhares)
    whole_value = whole.get_text().strip().replace(".", "")

    fraction_value = None
    if fraction:
        fraction_value = fraction.get_text().strip()

    # monta string tipo "346,73"
    if fraction_value:
        price_str = f"{whole_value},{fraction_value}"
    else:
        # fallback se fraction não existir
        price_str = f"{whole_value},00"

    return parse_price(price_str)


# ---------------------------------------------------------
# Scraper de um único produto
# ---------------------------------------------------------
def scrape_single_product(product: dict):
    name = product["name"]
    url = product["url"]
    target_price = product["target_price"]

    PRICE_SELECTOR = get_env_variable("PRICE_SELECTOR")

    html = fetch_html(url)
    if not html:
        return {
            "name": name,
            "url": url,
            "price": None,
            "target_price": target_price,
            "success": False,
        }


    if PRICE_SELECTOR == ".a-price-whole":
        price = extract_amazon_price(html)
        if price is not None:
            logger.info(f"Preço (Amazon) encontrado para {name}: {price}")
            return {
                "name": name,
                "url": url,
                "price": price,
                "target_price": target_price,
                "success": True,
            }
        else:
            logger.warning(f"Amazon fallback ativado para {name}")

    # Fallback genérico para outros sites
    price = extract_price_from_html(html, PRICE_SELECTOR)

    if price is None:
        logger.error(f"Preço não encontrado para: {name}")
        return {
            "name": name,
            "url": url,
            "price": None,
            "target_price": target_price,
            "success": False,
        }

    logger.info(f"Preço encontrado para {name}: {price}")
    return {
        "name": name,
        "url": url,
        "price": price,
        "target_price": target_price,
        "success": True,
    }



# Scraper de todos os produtos

def scrape_all_products():
    results = []
    for product in PRODUCTS:
        result = scrape_single_product(product)
        results.append(result)
    return results
