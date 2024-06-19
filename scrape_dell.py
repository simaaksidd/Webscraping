from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


base_url = 'https://www.dell.com/en-us/search/'

# We get this from the form
keyword = '1080p monitor'

def utf8_encoder(keyword, base_url):
    encoded_string = base_url + quote(keyword)
    return encoded_string 

def scrape_page(url):
    options = webdriver.SafariOptions()
    options.add_argument("userAgent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537")

    driver = webdriver.Safari(options=options)

    driver.get(url)

    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ps-title')))
    
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    grid = soup.find('div', class_='dell-ps ps')
    products = grid.find_all('article', class_='stack-accessories ps-stack')
    print(len(products))
    brands = []
    names = []
    prices = []
    urls = []
    for prod in products:
        heading = prod.find('h3', class_='ps-title')
        name = heading.find('a').text
        names.append(name)
        brand = name.split()[0]
        brands.append(brand)
        price_info = prod.find('div', class_='ps-dell-price ps-simplified')
        prices_info = price_info.find_all()
        if prices_info:
            price = price_info.find_all('span')[1].text
        else:
            price = price_info.text.split()[0]
        prices.append(price)
        link = heading.find('a').get('href')
        urls.append(link[2:])   
            
    # Store as JSON data
    data = [{"name": name, "price": price, "url": url} for name, price, url in zip(names, prices, urls)]
    output_path = os.path.join('webscraper', 'output_dell.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)      

url = utf8_encoder(keyword, base_url)


scrape_page(url)

#print(url)