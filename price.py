#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Apr 16, 2024 version of expedia

# import needed libraries
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
    'Departure': "LAX", 
    'Destination': "ABQ",
    'Date_leaving': "May 5, 2024",
    'Date_returning': "May 15, 2024"
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
    trip_date_return = flight_info['Date_returning']

    driver.get('https://www.expedia.com/');
    time.sleep(.5) 

    #click on flights
    flight_xpath = '//a[@aria-controls="search_form_product_selector_flights"]'
    flight_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, flight_xpath)))
    flight_element.click()
    time.sleep(.5)

    #click on roundtrip
    roundtrip_xpath = '//a[@aria-controls="FlightSearchForm_ROUND_TRIP"]'
    roundtrip_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, roundtrip_xpath)))
    time.sleep(.5)

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
        time.sleep(.05)
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
        time.sleep(.05)
    time.sleep(1)
    leaving_from_text_element.send_keys(Keys.DOWN, Keys.RETURN)
    time.sleep(1)

    """ get the appropriate dates of the flights """

    """ click on the departing date"""
    date_xpath = '//button[@data-stid="uitk-date-selector-input1-default"]'
    calender_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, date_xpath)))
    calender_element.click()
    time.sleep(.5)

    trip_date_xpath = '//div[contains(@aria-label, "{}")]/..'.format(trip_leave_date)

    departing_date_element = ""
    while departing_date_element == "":
        try:
            departing_date_element = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, trip_date_xpath)))
            departing_date_element.click() #Click on the departure date
        except TimeoutException:
           departing_date_element= ""
           next_month_xpath = '//button[@data-stid="uitk-calendar-navigation-controls-next-button"]'
           next_month_element = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, next_month_xpath)))
           next_month_element.click()
           time.sleep(1)
    
    """click on return date"""
    return_trip_date_xpath = '//div[contains(@aria-label, "{}")]/..'.format(trip_date_return)
    return_date_element = ""
    while return_date_element == "":
        try:
            return_date_element = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, return_trip_date_xpath)))
            return_date_element.click() #Click on the return date
        except TimeoutException:
           return_date_element= ""
           next_month_xpath = '//button[@data-stid="uitk-calendar-navigation-controls-next-button"]'
           next_month_element = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, next_month_xpath)))
           next_month_element.click()
           time.sleep(1)
    
    #exit out of the calender and return to the home page
    calender_element.send_keys(Keys.ESCAPE)

    """ click on finding flights"""
    search_flights_xpath = '//button[@id="search_button"]'
    search_flights_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, search_flights_xpath)))
    search_flights_element.click()
    time.sleep(15)

    """ sort the flights by lowest price"""
    nonstop_flights_xpath = '//input[@name="NUM_OF_STOPS"]'
    nonstop_flights_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, nonstop_flights_xpath)))
    if len(driver.find_elements(By.XPATH,nonstop_flights_xpath)) > 0:
        print("found nonstop flights")
        nonstop_flights_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, nonstop_flights_xpath)))
        nonstop_flights_element.click()
        time.sleep(1)
    time.sleep(1)

find_cheapest_flights(flight_inputs)