import bs4
import requests
import re
from entity import Author, Paper


def get_arxiv_info(tag: bs4.element.Tag) -> Paper:
    title = tag.find(class_="title").text.strip()
    authors = [
        t.strip() for t in tag.find(
            class_="authors").text.replace("Authors:", "").split(",")
    ]
    fields = [t.text for t in tag.find_all(class_="tag")]
    abstract = tag.find(class_="abstract-full").text[:-10].strip()
    abs_link = tag.find(href=re.compile("abs")).attrs["href"]
    pdf_link = tag.find(href=re.compile("pdf")).attrs["href"]
    return Paper(title, authors, fields, abstract, abs_link, pdf_link)


def get_scholar_info(tag: bs4.element.Tag):
    profile_link = tag.find(class_="gs_ai_name").a.attrs["href"]
    affiliation = tag.find(class_="gs_ai_aff").text
    interest = [x.text for x in tag.find_all(class_="gs_ai_one_int")]
    citation = int(tag.find(class_="gs_ai_cby").text[8:].strip())
    return Author(profile_link, affiliation, interest, citation)


def query_arxiv(keyword):
    site = "https://arxiv.org/search/"
    proxy = {"http": "127.0.0.1:7890"}
    params = {
        "query": keyword,
        "source": "header",
        "searchtype": "all",
    }
    r = requests.get(site, proxies=proxy, params=params)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    return soup


def query_scholar(author):
    site = "https://scholar.google.com/citations"
    proxy = {"http": "127.0.0.1:7890"}
    params = {
        "mauthors": author.replace(" ", "+"),
        "view_op": "search_authors",
        "hl": "en",
    }
    r = requests.get(site, proxies=proxy, params=params)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    return soup


soup = query_arxiv("cam")
page_results = soup.find_all("li", class_="arxiv-result")
papers = [get_arxiv_info(x) for x in page_results]

soup = query_scholar(papers[0].authors[0])
page_results = soup.find_all(class_="gs_ai_t")

