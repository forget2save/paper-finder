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
browser.close()

#%%

import os
import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.append(r"e:\fun\paper-finder")
from doc.utils import *
from gs.plaintext import *


url = "https://oaklandsok.github.io/"
xpath = "//tr//td/a"
save_path = r"f:\SoKs"
browser = start_browser(headless=True)
browser.get(url)
elems = browser.find_elements_by_xpath(xpath)
citation, titles = [], []
for elem in elems:
    title = elem.text
    link = elem.get_attribute("href")
    filename = os.path.join(save_path, filter_invalid_char(title+".pdf"))
    if not os.path.exists(filename):
        if "arxiv" in link:
            link = link.replace("abs", "pdf")
        print(link)
        try:
            download_pdf(link, filename)
        except:
            print("fail")
    titles.append(title)

# browser.back()
# for title in titles:
#     search_paper(browser, title)
#     info = get_info(browser)
#     citation.append((info[0], info[2]))
# citation.sort(key=lambda x: x[1], reverse=True)
# print(citation)
# browser.close()


# %%
