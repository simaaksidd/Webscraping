from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = 'https://www.nordstrom.com/sr?keyword='

# We get this from the form
keyword = 'black shirt'

def utf8_encoder(keyword, base_url):
    encoded_string = base_url + quote(keyword)
    return encoded_string 

def scrape_page(url):
    options = webdriver.SafariOptions()
    options.add_argument("userAgent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537")
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Safari(options=options)

    driver.get(url)

    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'kKGYj Y9bA4')))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    grid = soup.find('div', class_='gkAcy xHN13 liB50')
    products = grid.find_all()
    print(len(products))
    names = []
    prices = []
    urls = []
    '''for prod in products:
        price = prod.find('span', class_='styles_ProductPrice__KUcFU').text
        prices.append(price)
        name = prod.find('div', class_='styles_ResultItemTitleLink___CgWd undefined').text
        names.append(name)
        link = prod.find('a')
        link = link.get('href')
        link = 'https://www.nordstrom.com' + link
        urls.append(link)    
    # Store as JSON data
    data = [{"name": name, "price": price, "url": url} for name, price, url in zip(names, prices, urls)]
    output_path = os.path.join('webscraper', 'output_nord.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)
    '''
url = utf8_encoder(keyword, base_url)


scrape_page(url)

#print(url)