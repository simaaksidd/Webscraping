from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = 'https://www.oreillyauto.com/search?q='

# We get this from the form
keyword = 'door hinge'

def utf8_encoder(keyword, base_url):
    encoded_string = base_url + quote(keyword)
    return encoded_string 

def scrape_page(url):
    options = webdriver.SafariOptions()
    options.add_argument("userAgent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537")

    driver = webdriver.Safari(options=options)

    driver.get(url)

    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    #Price is loaded differently so we must add an explicit condition
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'js-ga-product-price')))

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('div', class_='product-row')
    names = []
    prices = []
    urls = []
    for row in rows:
        products = row.find_all('article', class_='product product--plp product--interchange js-product')
        for prod in products:     
            price_info = prod.find('div', class_='pricing-container')
            price = price_info.find('strong', class_='pricing_price js-ga-product-price').text
            prices.append(price)
            name = prod.find('h2', class_='js-product-name js-ga-product-name product__name').text
            names.append(name)
            link = prod.find('a', class_='js-product-link product__link')
            link = prod.a['href']
            link = 'https://www.oreillyauto.com' + link
            urls.append(link)   
            
    # Store as JSON data
    data = [{"name": name, "price": price, "url": url} for name, price, url in zip(names, prices, urls)]
    output_path = os.path.join('webscraper', 'output_oreilly.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)      
url = utf8_encoder(keyword, base_url)


scrape_page(url)