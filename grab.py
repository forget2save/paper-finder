import os
import time
import requests
from typing import List, Any, Dict
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys


def download_pdf(query: str, save_path: str, prefix: str):
    filename = "".join((c if c.isalnum() else "_" for c in query))
    filename = os.path.join(save_path, prefix + filename + ".pdf")
    if os.path.exists(filename):
        return

    elem = browser.find_element_by_xpath(search_xpath)
    elem: WebElement
    elem.clear()
    elem.send_keys(query)
    elem.send_keys(Keys.RETURN)
    elem = browser.find_element_by_xpath(result_xpath)
    link = elem.get_attribute("href")
    r_d = requests.get(link, stream=True)
    r_d: requests.Response
    with open(filename, "wb") as f:
        f.write(r_d.content)
    r_d.close()


def find_queries(query_file: str, verify: Any) -> List[str]:
    with open(query_file, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
    queries = []
    for l in lines:
        l = verify(l)
        if l:
            queries.append(l)
    return queries


def foo(line: str) -> str:
    if len(line) > 5 and line[0] == "-" and line[2] != "#":
        return line[2:]
    return ""


def find_venues(query_file: str) -> Dict[str, str]:
    with open(query_file, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
    venues = {}
    venue = "none"
    for line in lines:
        if len(line) > 5 and line[0] == "-" and line[2:5] == "###":
            venue = "".join((c for c in line[5:] if c.isalnum()))
        elif len(line) > 5 and line[0] == "-" and line[2] != "#":
            paper = line[2:]
            venues[paper] = venue
    return venues


if __name__ == "__main__":
    url = "https://scholar.google.com/scholar?hl=en&q=deep+learning"
    search_xpath = "//*[@id='gs_hdr_tsi']"
    result_xpath = "//*[@id='gs_res_ccl_mid']/div[1]/div[1]/div/div/a"
    driver_path = "F:/edgeDriver/msedgedriver.exe"
    query_file = "G:/logseq/pages/paper_list.md"
    save_path = "G:/20220126"

    fails = []
    browser = webdriver.Edge(driver_path)
    browser.get(url)
    queries = find_queries(query_file, foo)
    venues = find_venues(query_file)
    for query in queries:
        try:
            # print(query)
            prefix = venues[query]
            download_pdf(query, save_path, prefix)
        except Exception as e:
            # print(e)
            time.sleep(1)
            fails.append((prefix, query))
    browser.close()
    for f in fails:
        print(f)
