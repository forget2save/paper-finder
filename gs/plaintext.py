# coding:utf-8
#%%
import warnings
import requests
from typing import Tuple
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver

warnings.filterwarnings("ignore")


def start_browser(
        driverpath:
    str = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe",
        headless: bool = False) -> WebDriver:
    options = webdriver.ChromeOptions()
    options.headless = headless
    browser = webdriver.Chrome(driverpath, options=options)
    url = "https://scholar.google.com/scholar?hl=en&q=deep+learning"
    browser.get(url)
    return browser


def _get_citation(s: str) -> int:
    i = s.find("Cited by")
    j = s.find("Related")
    try:
        c = int(s[i + 8:j])
    except:
        return 0
    return c


def _get_authors(s: str) -> str:
    return s.split("-")[0].strip()


def get_info(browser: WebDriver) -> Tuple[str, str, int, str, str]:
    result_xpath = "//*[@id='gs_res_ccl_mid']/div"
    root: WebElement = browser.find_element_by_xpath(result_xpath)

    try:
        elem: WebElement = root.find_element_by_class_name("gs_rt")
        title = elem.text
        try:
            elem1: WebElement = elem.find_element_by_tag_name("a")
            title_link = elem1.get_attribute("href")
        except:
            title_link = ""
    except:
        title = ""
        title_link = ""

    try:
        elem = root.find_element_by_class_name("gs_or_ggsm")
        elem = elem.find_element_by_tag_name("a")
        asset_link = elem.get_attribute("href")
    except:
        asset_link = ""

    try:
        elem = root.find_element_by_class_name("gs_ri")
        try:
            elem1 = elem.find_element_by_class_name("gs_fl")
            citation = _get_citation(elem1.text)
        except:
            citation = 0
        try:
            elem2: WebElement = elem.find_element_by_class_name("gs_a")
            authors = _get_authors(elem2.text)
        except:
            authors = ""
    except:
        citation = 0
        authors = ""

    return title, authors, citation, title_link, asset_link


def search_paper(browser: WebDriver, query: str):
    search_xpath = "//*[@id='gs_hdr_tsi']"
    elem: WebElement = browser.find_element_by_xpath(search_xpath)
    elem.clear()
    elem.send_keys(query)
    elem.send_keys(Keys.RETURN)


def download_pdf(link: str, filename: str):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    try:
        proxies = {
            "http": None,
            "https": None,
        }
        r_d: requests.Response = requests.get(link,
                                              stream=True,
                                              headers=headers,
                                              proxies=proxies,
                                              timeout=10)
    except:
        try:
            proxies = {
                "http": "http://127.0.0.1:7890",
                "https": "http://127.0.0.1:7890",
            }
            r_d = requests.get(link,
                               stream=True,
                               headers=headers,
                               proxies=proxies,
                               timeout=10)
        except:
            raise NotImplementedError
    with open(filename, "wb") as f:
        f.write(r_d.content)
    r_d.close()
