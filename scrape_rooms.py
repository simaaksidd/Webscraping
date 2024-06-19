from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


base_url = 'https://www.roomstogo.com/search/?page=1&query='

# We get this from the form
keyword = 'black sofa'

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
    products = soup.find_all('div', class_='css-fb3dw2')

    names = []
    prices = []
    urls = []
    for prod in products:
        price = prod.find('span', class_='jss43').text
        prices.append(price)
        name = prod.find('h2', class_='MuiTypography-root MuiTypography-body1 css-p834i9').text
        names.append(name)
        link = prod.find('a', class_='MuiTypography-root MuiLink-root MuiLink-underlineHover jss15 product-image-link disable-underline MuiTypography-colorPrimary')
        link = link.get('href')
        link = 'https://www.roomstogo.com' + link
        urls.append(link)    
    # Store as JSON data
    data = [{"name": name, "price": price, "url": url} for name, price, url in zip(names, prices, urls)]
    output_path = os.path.join('webscraper', 'output_rooms.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)

url = utf8_encoder(keyword, base_url)


scrape_page(url)

#print(url)