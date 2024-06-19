from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re


base_url = 'https://www.macys.com/shop/featured/'

# We get this from the form
keyword = 'black shirt'

def utf8_encoder(keyword, base_url):
    encoded_string = base_url + quote(keyword)
    return encoded_string

def scrape_page(url):
    driver = webdriver.Safari()

    driver.get(url)

    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
   
    # One product has that other class
    products = soup.find_all('li', class_=['cell productThumbnailItem', 'cell productThumbnailItem sticky-header-observer'])
    
    brands = []
    names = []
    prices = []
    urls = []
    for prod in products:
        brand = prod.find('div', class_='productBrand').text
        brands.append(brand.strip())

        discount_span = prod.find('span', class_='discount')
        # for the products with discounted vs regular prices
        if discount_span:
            price = discount_span.text.strip()
            price = re.search(r'\d+\.\d+', price).group()
            prices.append(price)
        else:
            regular_span = prod.find('span', class_='regular')
            if regular_span:
                price = regular_span.text.strip()
                price = re.search(r'\d+\.\d+', price).group()
                prices.append(price)
        
        name = prod.find('a', class_='productDescLink productDescLinkEllipsis')
        name = name.get('title')
        names.append(name)
        
        link = prod.find('a', class_='productDescLink productDescLinkEllipsis')
        link = link.get('href')
        link = 'https://www.macys.com' + link
        urls.append(link)   
    # Store as JSON data
    data = [{"name": name, "price": price, "brand": brand, "url": url} for name, price, brand, url in zip(names, prices, brands, urls)]
    output_path = os.path.join('webscraper', 'output_macys.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)
url = utf8_encoder(keyword, base_url)


scrape_page(url)

print(url)