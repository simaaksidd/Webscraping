from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from urllib.parse import quote
import json 
import os
import re

base_url = 'https://tjmaxx.tjx.com/store/shop/?_dyncharset=utf-8&initSubmit=true&Ntt='

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'http://www.google.com/',
    'Connection': 'keep-alive'
}

# We get this from the form
keyword = 'black shirt'

def is_discounted(div):
    discount = div.find(attrs={'class': 'sr-only'}).contents[0]

def utf8_encoder(keyword, base_url):
    encoded_string = base_url + quote(keyword)
    return encoded_string

def scrape_page(url,):
    response = requests.get(url, headers=headers)

    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f'Got a 200 for {url}')
        names = []
        prices = []
        subtitles = []
        # Get prices and name and type
        # Find all rows with class "equal-height-row"
        rows = soup.find_all('div', class_='equal-height-row')
        for row in rows:
            # Find all products within the current row
            products = row.find_all('div', class_='product-inner')
            for product in products:
                # Extract the product title
                product_title = product.find('span', class_='product-title').text.strip()
                price  = product.find('span', class_='product-price').text
                names.append(product_title)
                if 'original price' in price:
                    # Define a regular expression pattern to match the new price
                    pattern = re.compile(r'\$[\d.]+')

                    # Find all matches in the input string
                    matches = pattern.findall(price)
                    # Keep only the second match
                    cleaned_string = matches[1] if len(matches) > 1 else ''
                    prices.append(cleaned_string)
                else:
                    prices.append(price)
        # Remove '\n' and '\t' from each element
        prices = [item.replace('\n', '').replace('\t', '') for item in prices]
        # Store as JSON data
        data = [{"name": name, "price": price} for name, price in zip(names, prices)]
        output_path = os.path.join('webscraper', 'output_tj.json')
        with open(output_path, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=3, ensure_ascii=False)
        # Rate limit
        time.sleep(2) 
    else:
        print(f'Error {response.status_code}')
        print(f"Failed to retrieve page: {url}")


url = utf8_encoder(keyword, base_url)


scrape_page(url)