# scraper/amazon_scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_amazon(listing_id):
    url = f"https://www.amazon.com/dp/{listing_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    price = soup.find("span", {"id": "priceblock_ourprice"})
    if price:
        return {"price": price.text.strip()}
    return {"price": "N/A"}
