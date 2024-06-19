from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


base_url = 'https://www.lowes.com/search?searchTerm='

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
    grid = soup.find('section', class_='items')
    products = grid.find_all('div', class_='sc-o9wle2-4')
    brands = []
    names = []
    prices = []
    urls = []
    for prod in products:
        brand = prod.find('span', class_='BrandNameStyle-sc-4v6c0e-3 ifIzUE expand-product-specs').text
        brands.append(brand)
        price_info = prod.find('div', class_='prdt-actl-pr ')
        price_dollars = price_info.find('span').text
        price_cents =  price_info.find_all('sup')[1].text
        price = f'${price_dollars}.{price_cents}'
        prices.append(price)
        name = prod.find('span', class_='description-spn').text
        names.append(name)
        a_tag = prod.find('div', class_='DescriptionHolderStyle-sc-4v6c0e-23 belDan ')
        link = a_tag.find('a').get('href')
        link = 'https://www.lowes.com' + link
        urls.append(link)   
            
    # Store as JSON data
    data = [{"name": name, "price": price, "url": url} for name, price, url in zip(names, prices, urls)]
    output_path = os.path.join('webscraper', 'output_lowes.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)      

url = utf8_encoder(keyword, base_url)


scrape_page(url)

#print(url)