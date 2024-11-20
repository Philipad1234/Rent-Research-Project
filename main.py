import requests
from details import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}


response = requests.get(ZILLOW_CLONE_URL, headers=header)

soup = BeautifulSoup(response.content, "html.parser")

prices = []
locations = []
links = []

price_list = soup.findAll('span', attrs={'class': 'PropertyCardWrapper__StyledPriceLine'})
location_list = soup.find_all('address')
links_list = soup.find_all('a', attrs={'class': 'StyledPropertyCardDataArea-anchor'})

for price in price_list:
    price_actual = price.getText()
    price_actual = price_actual.strip("+/mo1bd+ 1")
    prices.append(price_actual)

for location in location_list:
    actual_location = location.text.strip().replace("|", "")
    locations.append(actual_location)

for link in links_list:
    actual_link = link.get('href')
    links.append(actual_link)

listings = []

for price, location, link in zip(prices, locations, links):
    listing = {'price': price, 'location': location, 'link': link}
    listings.append(listing)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options)
driver.get(SPREADSHEET_URL)

for item in listings:
    sleep(3)
    address_input = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    address_input.send_keys(item['location'])
    price_input.send_keys(item['price'])
    link_input.send_keys(item['link'])
    submit_button.click()

    sleep(3)
    another_response = driver.find_element(By.CSS_SELECTOR, 'a')
    another_response.click()





