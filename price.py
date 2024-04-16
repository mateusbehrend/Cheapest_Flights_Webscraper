#!/usr/bin/env python3
# -*- coding: utf-8 -*-



# print(get_price())
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

import pandas as pd

import smtplib
from email.message import EmailMessage

import schedule

flight_inputs = {
    'Departure': "Los Angeles", 
    'Destination': "Santorini",
    'Date_leaving': "April 25, 2024",
    'Date_returning': "September 20, 2024"
}

def find_cheapest_flights(flight_info):
    print(flight_info)
    PATH = r'/Users/mateus/Desktop/personalProjects/chromedriver'
    # Create Chromeoptions instance 
    options = webdriver.ChromeOptions() 
    
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 
    
    # Setting the driver path and requesting a page 
    driver = webdriver.Chrome(options=options) 
    
    # Changing the property of the navigator value for webdriver to undefined 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    leaving_from = flight_info['Departure']
    going_to = flight_info['Destination']
    trip_leave_date = flight_info['Date_leaving']

    driver.get('https://www.expedia.com/');
    time.sleep(1) 

    #click on flights
    flight_xpath = '//a[@aria-controls="search_form_product_selector_flights"]'
    flight_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, flight_xpath)))
    flight_element.click()
    time.sleep(1)

    #click on roundtrip
    roundtrip_xpath = '//a[@aria-controls="FlightSearchForm_ROUND_TRIP"]'
    roundtrip_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, roundtrip_xpath)))
    time.sleep(1)

    """ fill out form for departure """
    #click on leaving from
    leaving_from_xpath = '//button[@aria-label="Leaving from"]'
    leaving_from_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, leaving_from_xpath)))
    # leaving_from_element.clear()
    leaving_from_element.click()
    print(leaving_from)
    print(leaving_from_element)
    leaving_from_text_xpath = '//input[@id="origin_select"]'
    leaving_from_text_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, leaving_from_text_xpath)))
    time.sleep(1)
    #leaving_from_text_element.send_keys(leaving_from)
    for i in range(len(leaving_from)):
        leaving_from_text_element.send_keys(leaving_from[i])
        time.sleep(.1)
    time.sleep(1)
    leaving_from_text_element.send_keys(Keys.DOWN,Keys.RETURN)
    time.sleep(1)

    """" fill out form for destination """
    going_to_xpath = '//button[@aria-label="Going to"]'
    going_to_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, going_to_xpath)))
    going_to_element.click()
    time.sleep(1)
    leaving_from_text_xpath = '//input[@id="destination_select"]'
    leaving_from_text_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, leaving_from_text_xpath)))
    time.sleep(1)
    for i in range(len(going_to)):
        leaving_from_text_element.send_keys(going_to[i])
        time.sleep(.1)
    time.sleep(1)
    leaving_from_text_element.send_keys(Keys.DOWN, Keys.RETURN)
    time.sleep(1)

    """ get the appropriate dates of the flights """
    date_xpath = '//button[@data-stid="uitk-date-selector-input1-default"]'
    departing_date_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, date_xpath)))
    departing_date_element.click()
    time.sleep(1)

    #trip_date_xpath = '//div[contains(@aria-label, "{}")]../..'.format(trip_leave_date)
    trip_date_xpath = '//div[contains(@aria-label, "{}")]/..'.format(trip_leave_date)
    print(trip_date_xpath)
    departing_date_element = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, trip_date_xpath)))
    print(departing_date_element.text)
    print(departing_date_element.tag_name)
    print(departing_date_element)
    #element = WebDriverWait(driver,3).until(EC.presence_of_element_located("//button[contains(@aria-label, 'April 30, 2024')"))
    departing_date_element.click()
    # departing_date_element = ""
    # while departing_date_element == "":
    #     try:
    #         departing_date_element = WebDriverWait(driver,3).until(
    #         EC.presence_of_element_located((By.XPATH, trip_date_xpath))
    #         )
    #         departing_date_element.click() #Click on the departure date
    #     except TimeoutException:
    #        departing_date_element=""
    #        next_month_xpath = '//button[@data-stid="date-selector-paging"][2]'
    #        driver.find_element(By.XPATH, next_month_xpath).click()
    #        time.sleep(1)
    
    # #depart_date_done_xpath = '//button[@data-stid="apply-date-picker"]'
    # driver.find_element(By.XPATH, '//button[@data-stid="apply-date-selector"]').click()
    
    departing_date_element.send_keys(Keys.ESCAPE)

    """ click on finding flights"""
    search_flights_xpath = '//button[@id="search_button"]'
    search_flights_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, search_flights_xpath)))
    search_flights_element.click()
    time.sleep(60)

find_cheapest_flights(flight_inputs)