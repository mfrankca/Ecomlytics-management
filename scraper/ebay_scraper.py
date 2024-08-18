# scraper/ebay_scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_ebay(listing_id):
    url = f"https://www.ebay.com/itm/{listing_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    price = soup.find("span", {"id": "prcIsum"})
    if not price:
        price = soup.find("span", {"id": "mm-saleDscPrc"})

    if price:
        price_text = price.text.strip().replace("US $", "")
        return {"price": price_text}
    return {"price": "N/A"}
