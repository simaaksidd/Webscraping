from bs4 import BeautifulSoup
from urllib.parse import quote
import json 
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

base_url = 'https://www.wayfair.com/keyword.php?keyword='

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
   
    # Grid div
    grid = soup.find('div', class_='kzv0b81_6101 kzv0b86e_6101 kzv0b81yc_6101 l5osrp1_6101 l5osrp3_6101')
    brands = []
    names = []
    prices = []
    urls = []
    if grid:
        # Find all divs within the grid because this website is garbage
        products = grid.find_all('div')
        print(products)

        # Iterate through the nested divs and print their text content
        for prod in products:
            brand = prod.find('p', class_=('_1vgix4w0_6101 _1vgix4w2_6101 _1vgix4w6_6101')).text
            brand = brand.replace('by ', '', 1)
            brands.append(brand)

            price = prod.find_all('span', class_='oakhm627_6101 oakhm6y5_6101 oakhm610g_6101 oakhm6aj_6101')[1]
            price = price.text
            prices.append(price)

            name = prod.find('span', class_='StyledBox-owpd5f-0 BoxV2___StyledStyledBox-sc-1wnmyqq-0 dDDqzx').text
            names.append(name)

            link = prod.find('a', class_='_1yxeg5wb_6101')
            link = link.get('href')
            urls.append(link)   
            print(f'Brand: {brand}, Price: {price}, Name: {name}, URL: {link}')
    else:
        print("Products not found.")
    # Store as JSON data
    data = [{"name": name, "price": price, "brand": brand, "url": url} for name, price, brand, url in zip(names, prices, brands, urls)]
    output_path = os.path.join('webscraper', 'output_wayfair.json')
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=3, ensure_ascii=False)
url = utf8_encoder(keyword, base_url)

if __name__ == '__main__':
    scrape_page(url)
    print(url)