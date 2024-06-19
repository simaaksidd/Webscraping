from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


base_url = 'https://www.homedepot.com/s/'

# We get this from the form
keyword = '26 ft. ladder'

def utf8_encoder(keyword, base_url):
    encoded_string = base_url + quote(keyword)
    return encoded_string 

def scrape_page(url):
    options = webdriver.SafariOptions()
    options.add_argument("userAgent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537")

    driver = webdriver.Safari(options=options)

    driver.get(url)

    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    grid1 = soup.find_all('section', class_='grid')[1]
    grid2 = soup.find_all('section', class_='grid')[2]
    products1 = grid1.find_all('div', class_='browse-search__pod col__12-12 col__6-12--xs col__4-12--sm col__3-12--md col__3-12--lg')
    products2 =  grid2.find_all('div', class_='placeholder-product-pod col__12-12 col__4-12--xs col__3-12--sm col__3-12--md col__3-12--lg')
    brands = []
    names = []
    prices = []
    urls = []
    for prod in products1:
        brand = prod.find('p', class_='product-header__title__brand--bold--4y7oa').text
        brands.append(brand)
        price_info = prod.find('div', class_='price-format__main-price')
        price_dollars = price_info.find_all('span')[1].text
        price_cents =  price_info.find_all('span')[3].text
        price = f'${price_dollars}.{price_cents}'
        prices.append(price)
        name = prod.find('span', class_='product-header__title-product--4y7oa').text
        names.append(name)
        link = prod.find('a', class_='product-image')
        link = prod.a['href']
        link = 'https://www.homedepot.com' + link
        urls.append(link)   
            
    # Store as JSON data
    data = [{"brand": brand, "name": name, "price": price, "url": url} for brand, name, price, url in zip(brands, names, prices, urls)]
    output_path = os.path.join('webscraper', 'output_homedepot.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)      
url = utf8_encoder(keyword, base_url)


scrape_page(url)