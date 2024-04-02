import time
import os.path
import logging
import unittest, time, re
import csv
import numpy as np
import pandas as pd
import sys
import time
import datetime
from os import fsync
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

## Setup chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless") # Ensure GUI is off
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

config = {
    'EMAIL': 'toth.virag@kerekparosklub.hu',
    'PASSWORD': 'Polo1234'
}

login_url = 'https://kerekparosklub.hu/login/admin'

# Get page
browser.get(login_url)

elem = browser.find_element(By.NAME, 'email')
elem.clear()
elem.send_keys(config['EMAIL'])
elem = browser.find_element(By.NAME, 'password')
elem.clear()
elem.send_keys(config['PASSWORD'])
elem.submit()

# Old API	New API
# find_element_by_id(‘id’)	find_element(By.ID, ‘id’)
# find_element_by_name(‘name’)	find_element(By.NAME, ‘name’)
# find_element_by_xpath(‘xpath’)	find_element(By.XPATH, ‘xpath’)
# get user page
elem = browser.find_element(By.XPATH,"//span[text()='FELHASZNÁLÓK']").click()
time.sleep(2)
elem = browser.find_element(By.XPATH,"//span[text()='Felhasználók']").click()

result = pd.read_csv('/home/adamr/project/adaminfo/selenium-kk/test.csv', dtype=str)
for d in result.values:
    print(d)
    if d[3] != 'FALSE':
        # go to Search menu, looking for csv\username@domain.com and click on Szerkesztés button
        elem = browser.find_element(By.XPATH,"//input[@class='form-control input-sm' and @type='search']")
        elem.clear()
        elem.send_keys(d[1])
        time.sleep(6)
        elem = browser.find_element(By.XPATH,"//a[text()=' Szerkesztés']").click()
        # modify user settings
        # copy-paste values from csv
        elem = browser.find_element(By.XPATH,"//input[@name='shipping_phone']").clear()
        elem = browser.find_element(By.XPATH,"//input[@name='shipping_phone']").send_keys(d[3])
        elem = browser.find_element(By.XPATH,"//input[@name='billing_phone']").clear()
        elem = browser.find_element(By.XPATH,"//input[@name='billing_phone']").send_keys(d[3])
        # copy-paste values based on get_attribute
        temp = browser.find_element(By.XPATH,"//input[@name='shipping_l_name']").get_attribute("value")
        elem = browser.find_element(By.XPATH,"//input[@name='billing_l_name']").clear()
        elem = browser.find_element(By.XPATH,"//input[@name='billing_l_name']").send_keys(temp)
        temp = browser.find_element(By.XPATH,"//input[@name='shipping_f_name']").get_attribute("value")
        elem = browser.find_element(By.XPATH,"//input[@name='billing_f_name']").clear()
        elem = browser.find_element(By.XPATH,"//input[@name='billing_f_name']").send_keys(temp)
        temp = browser.find_element(By.XPATH,"//input[@name='shipping_email']").get_attribute("value")
        elem = browser.find_element(By.XPATH,"//input[@name='billing_email']").clear()
        elem = browser.find_element(By.XPATH,"//input[@name='billing_email']").send_keys(temp)
        temp = browser.find_element(By.XPATH,"//input[@name='shipping_zip']").get_attribute("value")
        elem = browser.find_element(By.XPATH,"//input[@name='billing_zip']").clear()
        elem = browser.find_element(By.XPATH,"//input[@name='billing_zip']").send_keys(temp)
        temp = browser.find_element(By.XPATH,"//input[@name='shipping_city']").get_attribute("value")
        elem = browser.find_element(By.XPATH,"//input[@name='billing_city']").clear()
        elem = browser.find_element(By.XPATH,"//input[@name='billing_city']").send_keys(temp)
        temp = browser.find_element(By.XPATH,"//input[@name='shipping_address']").get_attribute("value")
        elem = browser.find_element(By.XPATH,"//input[@name='billing_address']").clear()
        elem = browser.find_element(By.XPATH,"//input[@name='billing_address']").send_keys(temp)
        # click on Mentés button
        elem = browser.find_element(By.XPATH,"//button[@type='submit' and text()='Mentés']").click()
        # go back to Felhasználók page
        elem = browser.find_element(By.XPATH,"//span[text()='Felhasználók']").click()

# Extract description from page and print
#description = browser.find_element(By.NAME, "description").get_attribute("content")
#print(f"{description}")

#Wait for 10 seconds
time.sleep(5)
browser.quit()

_LOGGER = logging.getLogger(__name__)