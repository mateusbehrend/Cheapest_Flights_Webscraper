#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import beautifulsoup4
# import requests
# from bs4 import BeautifulSoup


# def get_price():
#     url = 'https://www.amazon.com/AmazonBasics-File-Folders-Reinforced-Tab/dp/B01LYHE49W/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=LqkYs&content-id=amzn1.sym.5647ad7d-a084-4ecd-b845-9b7b054b6e4e%3Aamzn1.symc.1065d246-0415-4243-928d-c7025bdd9a27&pf_rd_p=5647ad7d-a084-4ecd-b845-9b7b054b6e4e&pf_rd_r=AN7RKFM6RY508RP5ZQBM&pd_rd_wg=WVCbA&pd_rd_r=20e18545-542e-4358-a523-00ae1c451f91&pd_rd_i=B01LYHE49W'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     price = soup.find(id='corePrice_desktop').get_text()
#     return price

# print(get_price())

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import pandas as pd

import smtplib
from email.message import EmailMessage

import schedule

departure_flight_inputs = {
    'Departure': " ORD", 
    'Destination': " LAX",
    'Date': "Jun 20, 2023"
}

return_flight_inputs = {
    'Departure': " LAX", 
    'Destination': " ORD",
    'Date': "Jun 20, 2023"
}

def find_cheapest_flights(flight_info):
    PATH = r'/Users/mateus/Desktop/personalProjects/chromedriver'
    driver = webdriver.Chrome()
    
    leaving_from = flight_info['Departure']
    going_to = flight_info['Destination']
    trip_date = flight_info['Date']

    driver.get('https://www.expedia.com/');
    time.sleep(2) 

    #click on flights
    flight_xpath = '//a[@aria-controls="search_form_product_selector_flights"]'
    flight_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, flight_xpath)))
    flight_element.click()
    time.sleep(2)

    #fill out form for departure and return
    #click on leaving from
    # leaving_from_xpath = 




find_cheapest_flights(departure_flight_inputs)