from scraper import scrape_all_products
from notifier import notify_price_drop
from utils import update_history
from config import PRODUCTS

def main():
    results = scrape_all_products()

    # salva histórico
    for item in results:
        if item["success"] and item["price"] is not None:
            update_history(item["name"], item["price"], item["url"])

    # notifica
    notify_price_drop(results, receiver_email="seuemail@gmail.com")


if __name__ == "__main__":
    main()
