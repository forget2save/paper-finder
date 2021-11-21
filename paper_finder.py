import bs4
import requests
import re


def get_arxiv_links(tag: bs4.element.Tag):
    title = tag.find(class_="title").text.strip()
    # don't worry! papers that have single author are also named by "authors" in arxiv.
    authors = [
        t.strip() for t in tmp.find(
            class_="authors").text.replace("Authors:", "").split(",")
    ]
    fields = [t.attrs["data-tooltip"] for t in tag.find_all(class_="tag")]
    abs_link = tag.find(href=re.compile("abs")).attrs["href"]
    pdf_link = tag.find(href=re.compile("pdf")).attrs["href"]
    return title, abs_link, pdf_link, fields, authors


proxy = {"http": "127.0.0.1:7890"}
arxiv = "https://arxiv.org/search/"
keyword = "cam"
params = {
    "query": keyword,
    "source": "header",
    "searchtype": "all",
}
r = requests.get(arxiv, proxies=proxy, params=params)
# https://arxiv.org/search/?query=cam&source=header&searchtype=all
soup = bs4.BeautifulSoup(r.text, "html.parser")
page_results = soup.find_all("li", class_="arxiv-result")
tmp = page_results[0]
get_arxiv_links(tmp)
