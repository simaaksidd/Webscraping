from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


base_url = 'https://www.dillards.com/search-term/'

# We get this from the form
keyword = 'black shirt'

def utf8_encoder(keyword, base_url):
    encoded_string = base_url + quote(keyword)
    return encoded_string + '?realSearch=Y'

def scrape_page(url):
    driver = webdriver.Safari()

    driver.get(url)

    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    products = soup.find_all('div', class_='col-sm-4 result-tile')
    
    brands = []
    names = []
    prices = []
    urls = []
    for prod in products:
        brand = prod.find('span', class_='brandName').text
        brands.append(brand)
        price = prod.find('span', class_='price').text
        prices.append(price)
        name = prod.find('span', class_='productName').text
        names.append(name)
        link = prod.find('a', class_='d-block tileImgLinkWrapper')
        link = link.get('href')
        link = 'https://www.dillards.com' + link
        urls.append(link)    
    # Store as JSON data
    data = [{"name": name, "price": price, "brand": brand, "url": url} for name, price, brand, url in zip(names, prices, brands, urls)]
    output_path = os.path.join('webscraper', 'output_dillards.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)

url = utf8_encoder(keyword, base_url)


scrape_page(url)

#print(url)