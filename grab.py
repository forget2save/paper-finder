# coding:utf-8
import os
import re
import time
import requests
from typing import List, Any, Dict
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys


def download_pdf(query: str, save_path: str, prefix: str):
    filename = os.path.join(save_path, prefix + query + ".pdf")
    if os.path.exists(filename):
        return

    elem = browser.find_element_by_xpath(search_xpath)
    elem: WebElement
    elem.clear()
    elem.send_keys(query)
    elem.send_keys(Keys.RETURN)
    elems = browser.find_elements_by_xpath(result_xpath)
    for elem in elems:
        link = elem.get_attribute("href")
        if "pdf" in link:
            r_d = requests.get(link, stream=True)
            r_d: requests.Response
            with open(filename, "wb") as f:
                f.write(r_d.content)
            r_d.close()
            break


def find_queries(query_file: str, verify: Any) -> List[str]:
    with open(query_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        lines = [l.strip("\n") for l in lines]
    queries = []
    for l in lines:
        l = verify(l)
        if l:
            queries.append(re.sub('[\\\/:*?"<>|]', "", l))
    return queries


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


def sort_md(file_path):
    lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        tmp = f.readlines()
        buf = ""
        for line in tmp:
            if line[0] != "-":
                buf += line
            else:
                if len(buf) > 5:
                    lines.append(buf)
                buf = line
        if len(buf) > 5:
            lines.append(buf)
    lines.sort()
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    url = "https://scholar.google.com/scholar?hl=en&q=deep+learning"
    search_xpath = "//*[@id='gs_hdr_tsi']"
    result_xpath = "//*[@id='gs_res_ccl_mid']/div[1]/div[1]/div/div/a"
    driver_path = "F:/edgeDriver/chromedriver.exe"

    query_file = "G:/obsidian/physical-adversarial-attack/LiDAR attacks.md"
    save_path = "G:/20220217"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    def foo(line: str) -> str:
        if len(line) > 5 and line[0] == "-":
            idx = line.find("*") - 1
            return line[2:idx]
        return ""

    summary = os.path.join(save_path, "summary.md")
    sort_md(summary)
    fails = []
    options = webdriver.ChromeOptions()
    options.headless = True
    browser = webdriver.Chrome(driver_path, options=options)
    browser.get(url)
    queries = find_queries(query_file, foo)
    # venues = find_venues(query_file)
    with open(summary, "a", encoding="utf-8") as f:
        for query in queries:
            f.write(f"- [{query}](./{query}.pdf)\n")
            try:
                # print(query)
                # prefix = venues[query]
                prefix = ""
                download_pdf(query, save_path, prefix)
            except Exception as e:
                f.write("\t- not found\n")
                fails.append((prefix, query))
    browser.close()
    for f in fails:
        print(f)
