
import logging
import os
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from config import LOG_FILE, HISTORY_CSV


# Logger
def setup_logger(log_file=LOG_FILE):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger("price_monitor")
    logger.setLevel(logging.INFO)

    # Formato do log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()


# CSV Histórico
def load_history(csv_path=HISTORY_CSV):
    """Carrega histórico CSV em memória. Retorna lista de dicionários."""
    history = []
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Converte preço para float
                row['price'] = float(row['price'])
                history.append(row)
    else:
        # Se não existe, cria arquivo com cabeçalho
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['date_time','product_name','price','url'])
            writer.writeheader()
    return history

def update_history(product_name, price, url, csv_path=HISTORY_CSV):
    """Adiciona nova entrada ao CSV de histórico."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date_time','product_name','price','url'])
        writer.writerow({
            'date_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'product_name': product_name,
            'price': price,
            'url': url
        })
    logger.info(f"Histórico atualizado: {product_name} - {price}")


# Parsing de preço

def parse_price(price_str):
    #Converte string de preço para float.

    # Remove tudo que não é número, vírgula ou ponto
    cleaned = ''.join(c for c in price_str if c.isdigit() or c in [',','.'])
    # Substitui vírgula por ponto
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        logger.error(f"Não foi possível converter preço: {price_str}")
        return None


# HTML Helper

def extract_price_from_html(html_content, css_selector):
    """
    Recebe HTML e CSS selector, retorna preço como float.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    element = soup.select_one(css_selector)
    if not element:
        logger.error(f"Elemento não encontrado para selector: {css_selector}")
        return None
    return parse_price(element.get_text())
