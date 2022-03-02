# %%
import os
import re
import time
import requests
import shutil
import logging
from glob import glob
from typing import List, Any, Dict
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
logging.basicConfig(level=logging.INFO)

# %%
filter_invalid_char = lambda x: re.sub('[\\\/:*?"<>|]', "", x)
scihub_url = "https://sci-hub.se/"
goosch_url = "https://scholar.google.com/scholar?hl=en&q=deep+learning"
driver_path = "F:/edgeDriver/chromedriver.exe"
query_file = r"G:/obsidian/physical-adversarial-attack/LiDAR attacks.md"
save_path = r"G:/20220209"
if not os.path.exists(save_path):
    os.makedirs(save_path)
options = webdriver.ChromeOptions()
options.headless = False
browser = webdriver.Chrome(driver_path, options=options)
browser.get(goosch_url)

search_xpath = "//*[@id='gs_hdr_tsi']"  # google scholar
result_xpath = "//*[@id='gs_res_ccl_mid']/div"
with open(query_file, "r") as f:
    lines = [line[2:].split("*")[:2] for line in f.readlines()]
names = [filter_invalid_char(y.strip() + " " + x.strip()) for x, y in lines]

# %%
for name, (line, _) in zip(names, lines):
    pdfname = os.path.join(save_path, name + ".pdf")
    if os.path.exists(pdfname):
        continue
    
    elem = browser.find_element_by_xpath(search_xpath)
    elem.clear()
    elem.send_keys(line)
    elem.send_keys(Keys.RETURN)
    root = browser.find_element_by_xpath(result_xpath)
    try:
        elem = root.find_element_by_class_name("gs_or_ggsm")
        elem = elem.find_element_by_tag_name("a")
        link = elem.get_attribute("href")

        r_d = requests.get(link, stream=True)
        with open(pdfname, "wb") as f:
            f.write(r_d.content)
        r_d.close()
    except:
        elem = root.find_element_by_class_name("gs_rt")

# %%
browser.close()

# %%
scihub_url = "https://sci-hub.se/"
goosch_url = "https://scholar.google.com/scholar?hl=en&q=deep+learning"
driver_path = "F:/edgeDriver/chromedriver.exe"
query_file = "./papers.md"
save_path = "G:/20220208"
downloads = "C:/Users/zhu/Downloads/*.pdf"
olds = set(glob(downloads))

# %%
search_xpath = "//*[@id='gs_hdr_tsi']" # google scholar
search_xpath2 = '//*[@id="input"]/form/input[2]' # sci-hub
result_xpath = "//*[@id='gs_res_ccl_mid']/div"
nextpage_xpath = '//*[@id="gs_nm"]/button[2]'
citeby_xpath = '//*[@id="gs_res_ccl_mid"]/div/div[2]/div[3]/a[3]'

# %%
with open(query_file, "r") as f:
    lines = [line.strip() for line in f.readlines() if len(line) > 10]
    lines = [filter_invalid_char(line) for line in lines]
for name in lines:
    dir_name = os.path.join(save_path, name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# %%
options = webdriver.ChromeOptions()
options.headless = False
options.add_experimental_option(
    'prefs',
    {
        "download.prompt_for_download": False,  #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
browser = webdriver.Chrome(driver_path, options=options)

# %%
lines[3]

# %%
storage = {}

# %%
line = lines[1]
# citeby_xpath = '//*[@id="gs_res_ccl_mid"]/div/div/div[3]/a[3]'

with open("log.txt", "a") as f:
    f.write(line + "\n")
if line in storage:
    titles, links = storage[line]
    logging.warning(f"find cache! total num:{len(titles)}")
else:
    logging.warning("go to google scholar")
    browser.get(goosch_url)
    elem = browser.find_element_by_xpath(search_xpath)
    elem.clear()
    elem.send_keys(line)
    elem.send_keys(Keys.RETURN)

    elem = browser.find_element_by_xpath(citeby_xpath)
    counts = int("".join(x for x in elem.text if x.isdigit()))
    url = elem.get_attribute("href")
    browser.get(url)

    titles = []
    links = []

    while counts > 0:
        results = browser.find_elements_by_xpath(result_xpath)
        counts -= len(results)

        for elem in results:
            elem: WebElement
            elem = elem.find_element_by_class_name("gs_rt")
            try:
                elem = elem.find_element_by_tag_name("a")
                title = elem.text
                link = elem.get_attribute("href")
                titles.append(title)
                links.append(link)
            except Exception as e:
                logging.warning(elem.text)

        elem = browser.find_element_by_xpath(nextpage_xpath)
        elem.click()
        time.sleep(1)
    storage[line] = (titles, links)

logging.warning("go to sci-hub")
for title, link in zip(titles, links):
    pdfname = filter_invalid_char(title) + ".pdf"
    pdfname = os.path.join(save_path, line, pdfname)
    if os.path.exists(pdfname):
        # logging.warning("[already exist]" + title)
        continue
    if link[-4:] == ".pdf":
        r_d = requests.get(link, stream=True)
        with open(pdfname, "wb") as f:
            f.write(r_d.content)
        r_d.close()
        continue
    try:
        browser.get(scihub_url)
        elem = browser.find_element_by_xpath(search_xpath2)
    except Exception as e:
        time.sleep(60)
        browser.get(scihub_url)
        elem = browser.find_element_by_xpath(search_xpath2)
    elem.clear()
    elem.send_keys(link)
    elem.send_keys(Keys.RETURN)
    time.sleep(5)

    try:
        elem = browser.find_element_by_xpath('//*[@id="buttons"]/button')
        elem.click()

        prev_num = len(olds)
        now_num = prev_num
        while now_num == prev_num:
            all_pdf = glob(downloads)
            now_num = len(all_pdf)
            time.sleep(1)

        for name in all_pdf:
            if name not in olds:
                shutil.copy(name, pdfname)
                olds.add(name)
                break
    except Exception as e:
        with open("log.txt", "a") as f:
            f.write(title + "\n")
            f.write(link + "\n")

# %%
for line, v in storage.items():
    titles, links = v
    for title, link in zip(titles, links):
        pdfname = filter_invalid_char(title) + ".pdf"
        pdfname = os.path.join(save_path, line, pdfname)
        if not os.path.exists(pdfname):
            with open(pdfname, "wb") as f:
                pass

# %%
url = "https://scholar.google.com/scholar?hl=en&q=deep+learning"
search_xpath = "//*[@id='gs_hdr_tsi']"
result_xpath = "//*[@id='gs_res_ccl_mid']/div[1]/div[1]/div/div/a"
driver_path = "F:/edgeDriver/chromedriver.exe"
query_file = "G:/logseq/pages/paper_list.md"
save_path = "G:/20220126"

options = webdriver.ChromeOptions()
options.headless = False
browser = webdriver.Chrome(driver_path, options=options)
browser.get(url)

# %%
elem = browser.find_element_by_xpath(search_xpath)
elem.clear()
elem.send_keys("adversarial patch")
elem.send_keys(Keys.RETURN)

# %%
elems = browser.find_elements_by_xpath('//*[@id="gs_res_ccl_mid"]/div[1]/div[1]/div/div/a')
# elem.get_attribute("href")
for elem in elems:
    link = elem.get_attribute("href")
    if "pdf" in link:
        r_d = requests.get(link, stream=True)
        with open("./test/1.pdf", "wb") as f:
            f.write(r_d.content)
        r_d.close()
        break

# %%
def download_pdf(query: str, save_path: str, prefix: str):
    elem = browser.find_element_by_xpath(search_xpath)
    elem: WebElement
    elem.clear()
    elem.send_keys(query)
    elem.send_keys(Keys.RETURN)
    elem = browser.find_element_by_xpath(result_xpath)
    link = elem.get_attribute("href")
    r_d = requests.get(link, stream=True)
    r_d: requests.Response
    query = "".join((c if c.isalnum() else "_" for c in query))
    print(query)
    filename = os.path.join(save_path, query + ".pdf")
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

# %%
query_file = "G:/logseq/pages/paper_list.md"
save_path = "G:/20220126"
queries = find_queries(query_file, foo)
for query in queries:
    try:
        download_pdf(query, save_path)
        time.sleep(0.5)
    except Exception as e:
        print(e)

# %%
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
            paper = "".join((c if c.isalnum() else "_" for c in paper))
            venues[paper] = venue
    return venues

# %%
from glob import glob

files = glob(save_path+"/*.pdf")
venues = find_venues(query_file)
for name in files:
    folder, x = os.path.split(name)
    y = x[:-4]
    if y in venues:
        newname = os.path.join(folder, venues[y]+x)
        os.rename(name, newname)
    else:
        print(name)

# %%
query = "Back to the Drawing Board: A Critical Evaluation of Poisoning Attacks on Federated Learning"
save_path = "G:/20220126"
download_pdf(query, save_path)

# %%
browser.close()


