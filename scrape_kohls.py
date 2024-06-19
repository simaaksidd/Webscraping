from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


base_url = 'https://www.kohls.com/search.jsp?submit-search=web-regular&search='

# We get this from the form
keyword = 'black shirt'

def utf8_encoder(keyword, base_url):
    encoded_string = base_url + quote(keyword)
    return encoded_string 

def scrape_page(url):
    driver = webdriver.Safari()

    driver.get(url)

    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'prod_nameBlock')))

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    products = soup.find_all('li', class_='products_grid')
    print(len(products))
    names = []
    prices = []
    urls = []
    for prod in products:
        info = prod.find('div', class_='prod_nameBlock')
        price = prod.find('span', class_='prod_price_amount').text
        prices.append(price)
        name = info.find('p').text
        names.append(name.strip())
        link_info = prod.find('div', class_='prod_img_block')
        link = link_info.find('a')
        link = link.get('href')
        link = 'https://www.kohls.com' + link
        urls.append(link)    
    # Store as JSON data
    data = [{"name": name, "price": price, "url": url} for name, price, url in zip(names, prices, urls)]
    output_path = os.path.join('webscraper', 'output_kohls.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)

url = utf8_encoder(keyword, base_url)


scrape_page(url)

#print(url)