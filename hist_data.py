import json
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import lxml
import urllib.request as ur
import warnings
import openpyxl
import xlsxwriter
import time
from selenium.webdriver.common.keys import Keys
import datetime
import numpy as np
from tabulate import tabulate
from varname import argname2 
from pandas import DataFrame
import inspect
from urllib.parse import urlparse
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains


def Historical_Extract(Company_name):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--output=/dev/null")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    URL_Hist = "https://finance.yahoo.com/quote/" + Company_name + "/history"
    driver.get(URL_Hist)

    html = driver.execute_script('return document.body.innerHTML;')
    # BeautifulSoup the xml
    income_soup = BeautifulSoup(html, 'lxml')
    time.sleep(3)
    html2 = driver.find_element_by_tag_name('html')

    WebDriverWait(driver, 10)
    time.sleep(3)

    Time_Period_click = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div')
    action = ActionChains(driver)
    action.click(on_element = Time_Period_click)
    action.perform()

    Max_Data = driver.find_element_by_xpath('//*[@id="dropdown-menu"]/div/ul[2]/li[2]/button')
    action = ActionChains(driver)
    action.click(on_element = Max_Data)
    action.perform()

    Apply = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')
    action = ActionChains(driver)
    action.click(on_element = Apply)
    action.perform()


    

    time.sleep(1)

    startyear_str = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/span').text
    startyear = startyear_str[8:12]



    time.sleep(3)
    today = date.today()
    endyear = today.strftime("%Y")
    
    #if 5 years data then scroll till x = 150
    yeardiff = int(endyear) - int(startyear)

    if(yeardiff<=5):
        yeardiffscroll = 150
    elif(yeardiff>5 and yeardiff<=10):
        yeardiffscroll = 320
    elif(yeardiff>10 and yeardiff<=15):
        yeardiffscroll = 470
    elif(yeardiff>15 and yeardiff<=20):
        yeardiffscroll = 620
    elif(yeardiff>20 and yeardiff<=25):
        yeardiffscroll = 770
    elif(yeardiff>25 and yeardiff<=30):
        yeardiffscroll = 920
    elif(yeardiff>30 and yeardiff<=35):
        yeardiffscroll = 1070
    elif(yeardiff>36):
        yeardiffscroll = 2000

    x = 0
    while(x!=yeardiffscroll):
        html2.send_keys(Keys.PAGE_DOWN)
        x = x + 1

    html = driver.execute_script('return document.body.innerHTML;')
    # BeautifulSoup the xml
    income_soup = BeautifulSoup(html, 'lxml')

    # Find all HTML data structures that are tds
    hist_list = []
    for div in income_soup.find_all('td'):
        hist_list.append(div.text)


    #print(hist_list)

    #Move all the dividends info to Dividends List and delete all the useless info in the end of the hist_list
    Dividends_hist = []
    Stock_Split = []
    #Remove dividend rows
    for i_hist,val in enumerate(hist_list):
        if("Dividend" in val):
            Dividends_hist.append(hist_list[i_hist-1:i_hist+1])
            del hist_list[i_hist-1:i_hist+1]
            # print("Success")
        elif("Stock Split" in val):
            Stock_Split.append(hist_list[i_hist-1:i_hist+1])
            del hist_list[i_hist-1:i_hist+1]
        elif("*Close price adjusted for splits" in val):
            del hist_list[i_hist:]


    #print(Dividends_hist)
    #print(hist_list)

    #Sort the main list Row_Wise
    hist_list_final = []


    hist_list_final = list(zip(*[iter(hist_list)]*7))

    #Make a dataframe of the sorted list
    hist_df = pd.DataFrame(hist_list_final,columns=['Date', 'Open','High','Low','Close','AdjClose','Volume'])
    for col in hist_df.columns[1:]:                  # UPDATE ONLY NUMERIC COLS 
        try:
            hist_df[col] = hist_df[col].str.replace(',', '').astype(float)
            #print(hist_df[col])
        except:
            hist_df.loc[hist_df[col] == '-', col] = np.nan    # REPLACE HYPHEN WITH NaNs
            
    #print(hist_df)
    hist_df_json = json.loads(hist_df.to_json(orient='records'))

    return hist_df_json
