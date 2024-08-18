# scraper/walmart_scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_walmart(listing_id):
    url = f"https://www.walmart.com/ip/{listing_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    price = soup.find("span", {"class": "price-characteristic"})
    if price:
        price_text = price['content']
        return {"price": price_text}
    return {"price": "N/A"}
