from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from urllib.parse import quote
import json 
import os

base_url = 'https://www.nike.com/w?q='

# We get this from the form
keyword = 'air force 1'

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
        subtitles = []
        # Get prices and name and type
        for div in soup.findAll('div', attrs={'class':'product-card product-grid__card css-1t0asop'}):
            name = div.find('a').contents[0]
            names.append(name)
            price = div.find(attrs={'class': 'is--current-price'}).contents[0]
            prices.append(price)
            subtitle = div.find(attrs={'class': 'product-card__subtitle'}).contents[0]
            subtitles.append(subtitle)
        # Store as JSON data
        data = [{"name": name, "price": price, "subtitle": subtitle} for name, price, subtitle in zip(names, prices, subtitles)]
        output_path = os.path.join('webscraper', 'output_nike.json')
        with open(output_path, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=3, ensure_ascii=False)
        # Rate limit
        time.sleep(2) 
    else:
        print(f'Error {response.status_code}')
        print(f"Failed to retrieve page: {url}")


url = utf8_encoder(keyword, base_url)


scrape_page(url)

#print(url)