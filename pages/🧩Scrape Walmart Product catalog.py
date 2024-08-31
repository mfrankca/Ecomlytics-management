# scraper/walmart_scraper.py

import streamlit as st
import pandas as pd
import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import os

def display_sidebar():
    """
    Display the sidebar with a logo image and documentation.
    """
    image_path = "Logo/Ecomlytics1.png"
    # Sidebar content
    st.sidebar.image(image_path, width=150)  # Adjust the width to your preference
    st.sidebar.title("Ecomlytics")
    st.sidebar.write("Your partner in e-commerce analytics.")
    
    with st.sidebar.expander("Documentation", icon="📚"):
       st.write("""
        **Welcome to the SunRayCity Management Tool**

        ### About SunRayCity Sunglasses
        At SunRayCity Sunglasses, we search the world for the best deals on fashion and sport sunglasses. We only sell authentic and brand name sunglasses. If you are searching for a specific model that you cannot find on the site, send us an email at [sales@sunraycity.com](mailto:sales@sunraycity.com) and we will do our best to find it. We operate online only to offer these deals.

        ### Features
        - **Manage Customers**: Keep track of customer details and interactions.
        - **Product Catalog Management**: Maintain and update the product catalog.
        - **eBay Product Catalog Scraping**: Scrape product data from eBay.
        - **Scrape eBay Reviews**: Scrape reviews from the following eBay feedback pages:
          - [SunRayCity eBay Store 1](https://www.ebay.com/fdbk/feedback_profile/sunraycity)
          - [SunRayCity eBay Store 2](https://www.ebay.com/fdbk/feedback_profile/sunraycity_store)
        - **Compare Product Catalogs**: Compare the product catalog on eBay vs. the SunRayCity website.

        ### Instructions
        1. **Choose Site**: Select which eBay feedback site to scrape.
        2. **Enter URL**: Provide the URL of the eBay feedback page.
        3. **Scrape Data**: Click "Scrape Data" to collect and save reviews.

        Supported feedback sites: **eBay Feedback Site 1**, **eBay Feedback Site 2**.
        """)
       
       

def scrape_walmart(item):
   # url = f"https://www.walmart.com/ip/{listing_id}"
    #headers = {"User-Agent": "Mozilla/5.0"}
    keywords_filename = "keywords.txt"  
    output_filename = "output_links.txt"  
    base_url = "https://www.walmart.com/search"
    row = {'Listing ID': item}
    with open(input_filepath, 'r') as file:
      keywords = [line.strip() for line in file]

    search_links = [f"{base_url}?q={urllib.parse.quote(keyword)}" for keyword in keywords]
    all_absolute_links = []
    for link in search_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        
    absolute_links = [a['href'] for a in soup.find_all('a', class_='absolute', href=True)]
    try:
        title_element = soup.find('h1', attrs={'itemprop': 'name'}).text
        row['Title'] = title_element.text.replace('Details about', '').strip() if title_element else 'Not Available'
    except AttributeError:
          row['Title'] = 'Not Available' 
    return row      
        #reviews = soup.find('a', attrs={'itemprop': 'ratingCount'}).text
        #rating = soup.find('span', attrs={'class': 'rating-number'}).text
    #absolute_links = [url if url.startswith("https://") else "https://" + url for url in absolute_links]    
    #response = requests.get(url, headers=headers)
    #soup = BeautifulSoup(response.content, "html.parser")

    #price = soup.find("span", {"class": "price-characteristic"})
    
    #if price:
    #    price_text = price['content']
    #    return {"price": price_text}
    #return {"price": "N/A"}
# Determine the file type and read the data accordingly
def perform_web_scraping(input_filepath):
    _, file_extension = os.path.splitext(input_filepath)
    
    if file_extension == '.csv':
        listings = pd.read_csv(input_filepath)
    elif file_extension == '.txt':
        listings = pd.read_csv(input_filepath, header=None, names=['item'])
    else:
        st.error("Unsupported file type. Please upload a CSV or TXT file.")
        return []

    data = []
    for item in listings['item']:
        item_data = scrape_walmart(item)
        data.append(item_data)

    return data

def generate_output_files(data, output_format):
    output_files = []
    df = pd.DataFrame(data)

  
    # Generate the output files in the selected format(s)
    if 'Excel' in output_format:
        excel_file = 'output.xlsx'
        df.to_excel(excel_file, index=False)
        output_files.append(excel_file)
        
    if 'JSON' in output_format:
        json_file = 'output.json'
        df.to_json(json_file, orient='records')
        output_files.append(json_file)
        
    if 'CSV' in output_format:
        csv_file = 'output.csv'
        df.to_csv(csv_file, index=False)
        output_files.append(csv_file)

    return output_files


#image_path = "uploads//logo.png"
#st.sidebar.image(image_path, use_column_width=True)
#st.title("Welcome to SunRayCity Management")  

st.title('Ecomlytics managment App')
st.write('Upload a file with listing numbers and select the output file format.')
display_sidebar()
uploaded_file = st.file_uploader('Choose a file', type=['csv', 'txt'])
output_format = st.multiselect('Select output format', ['Excel', 'JSON', 'CSV'])

if uploaded_file is not None:
    if st.button('Scrape Data'):
        # Save uploaded file temporarily
        input_filepath = os.path.join('temp', uploaded_file.name)
        with open(input_filepath, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Perform web scraping
        data = perform_web_scraping(input_filepath)

        if data:
            # Generate output files
            output_files = generate_output_files(data, output_format)

            st.success('Scraping and file generation completed successfully!')

            for file in output_files:
                with open(file, 'rb') as f:
                    btn = st.download_button(
                        label=f"Download {file}",
                        data=f,
                        file_name=file,
                        mime='application/octet-stream'
                    )

if not os.path.exists('temp'):
    os.makedirs('temp')

