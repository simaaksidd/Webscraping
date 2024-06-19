from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from urllib.parse import quote
import json
import os

base_url = 'https://us.shein.com/pdsearch/'

# We get this from the form
keyword = 'black shirt'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'http://www.google.com/',
    'Connection': 'keep-alive'
}


def utf8_encoder(keyword, base_url):
    encoded_string = base_url + quote(keyword)
    return encoded_string

def scrape_page(url):
    response = requests.get(url, headers=headers)

    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f'Got a 200 for {url}')
        names = []
        prices = []
        # Get prices and name
        for sec in soup.findAll('section', attrs={'class':'product-card j-expose__product-item hover-effect product-list__item product-list__item-new'}):
            name = sec.find('a', attrs={'class':'goods-title-link--jump goods-title-link'}).contents[1]
            names.append(name)
            s = sec.find('p', attrs={'class':'product-item__camecase-wrap'})
            soup2 = BeautifulSoup(str(s), 'html.parser')
            price = soup2.find('span').text
            prices.append(price)
        # Store as JSON data
        data = [{"name": name, "price": price} for name, price in zip(names, prices)]
        output_path = os.path.join('webscraper', 'output_shein.json')
        with open(output_path, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)
        # Rate limit
        time.sleep(2) 
    else:
        print(f'Error {response.status_code}')
        print(f"Failed to retrieve page: {url}")


url = utf8_encoder(keyword, base_url)

scrape_page(url)