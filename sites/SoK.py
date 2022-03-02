#%%
# coding:utf-8
import os
import re
import time
import requests
from typing import List, Any, Dict
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

driver_path = "F:/edgeDriver/chromedriver.exe"
options = webdriver.ChromeOptions()
options.headless = False
browser = webdriver.Chrome(driver_path, options=options)

url = "https://oaklandsok.github.io/"
browser.get(url)
#%%
browser.close()
