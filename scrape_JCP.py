from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


base_url = 'https://www.jcpenney.com/s?searchTerm='

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

    products = soup.find_all('li', class_='pAB7b D2LxB gQ4Qt QLk4z false ZJiUp false false')
    
    names = []
    prices = []
    urls = []
    for prod in products:
        price = prod.find('span', class_='k26R9').text
        prices.append(price)
        name = prod.find('a', class_='-zrMP FMQQD t689a PI6hD SZ2pn SuQAn').text
        names.append(name)
        link = prod.find('a', class_='-zrMP FMQQD t689a PI6hD SZ2pn SuQAn')
        link = link.get('href')
        link = 'https://www.jcpenney.com' + link
        urls.append(link)    
    # Store as JSON data
    data = [{"name": name, "price": price, "url": url} for name, price, url in zip(names, prices, urls)]
    output_path = os.path.join('webscraper', 'output_JCP.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)

url = utf8_encoder(keyword, base_url)


scrape_page(url)

#print(url)