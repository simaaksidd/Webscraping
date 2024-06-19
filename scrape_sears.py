from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


base_url = 'https://www.sears.com/search='

# We get this from the form
keyword = 'cooler'

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
    grid = soup.find('div', class_='product-wrapper-grid')
    products = grid.find_all('div', class_=['col-grid-box','col-md-6', 'ng-star-inserted'])
    #print(products)
    print(grid)
    brands = []
    names = []
    prices = []
    urls = []
    '''for prod in products:
        name = prod.find('a', class_='mz-productlisting-title').text
        names.append(name)
        brand = name.split()[0]
        brands.append(brand)
        price = prod.find('span', class_='custom-price mz-price').text
        prices.append(price)
        a_tag = prod.find('div', class_='mz-productlisting-title')
        link = a_tag.find('a').get('href')
        urls.append(link)   
            
    # Store as JSON data
    data = [{"name": name, "price": price, "url": url} for name, price, url in zip(names, prices, urls)]
    output_path = os.path.join('webscraper', 'output_ace.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)      
'''
url = utf8_encoder(keyword, base_url)


scrape_page(url)

#print(url)