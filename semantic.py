import requests
import re
import os
import bs4
from typing import Dict, List

proxy = {"http": "127.0.0.1:7890"}
api_url = "https://api.semanticscholar.org/graph/v1"
arxiv_url = "https://arxiv.org"
paper_search_url = "/".join([api_url, "paper", "search"])
paper_detail_url = lambda paper_id: "/".join([api_url, "paper", paper_id])
paper_author_url = lambda paper_id: "/".join(
    [api_url, "paper", paper_id, "authors"])
paper_cite_url = lambda paper_id: "/".join(
    [api_url, "paper", paper_id, "citations"])
paper_refer_url = lambda paper_id: "/".join(
    [api_url, "paper", paper_id, "references"])
author_detail_url = lambda author_id: "/".join([api_url, "author", author_id])
author_paper_url = lambda author_id: "/".join(
    [api_url, "author", author_id, "papers"])
arxiv_pdf_url = lambda arxiv_id: "/".join(arxiv_url, "pdf", arxiv_id)

# web_url = "https://www.semanticscholar.org/search"

# r = requests.get(web_url, proxies=proxy, params={"q":"adversarial"}, headers={"User-Agent":"Mozilla/5.0"})
# soup = bs4.BeautifulSoup(r.text, "html.parser")
# print(soup)
r = requests.get(paper_search_url,
                 proxies=proxy,
                 params={
                     "query": "adversarial+attack+physical",
                     "fields": "title,externalIds,fieldsOfStudy,citationCount",
                     "limit": "100"
                 })

js : dict
js = r.json()


# print(js)
print(js["total"], js.keys())
print(len(js["data"]))
print(js["data"][0].keys())

# r = requests.get("https://arxiv.org/pdf/1607.02533", stream=True)

# with open(f"./{js['data'][0]['title']}.pdf", "wb") as f:
#     f.write(r.content)
