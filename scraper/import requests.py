import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_amazon_reviews(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    reviews = []
    for review in soup.find_all('span', {'data-asin': True}):
        text = review.get_text()
        reviews.append(text)
    
    return pd.DataFrame(reviews, columns=['Review'])
