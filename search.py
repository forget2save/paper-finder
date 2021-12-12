import requests
import time
from storage import author_database
from typing import Dict, List, Any


class APILimit:
    def __init__(self, speed) -> None:
        self.start = time.time()
        self.speed = speed
        self.cnt = 0
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        now = time.time()
        if now - self.start > self.speed * self.cnt:
            self.cnt += 1
            if now - self.start > 300:
                self.start = now
                self.cnt = 0
        else:
            time.sleep(1)
            self.__call__()


api_limit = APILimit(3)
api_url = "https://api.semanticscholar.org/graph/v1"
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

main_param = {
    "query": "",
    "fields":
    "title,venue,year,fieldsOfStudy,abstract,externalIds,citationCount,authors",
    "limit": "100",
    "offset": "0",
}

author_param = {
    "fields": "paperCount,citationCount,hIndex",
}


def search(keyword, p=None):
    if not p:
        p = main_param.copy()
    p["query"] = keyword
    api_limit()
    r = requests.get(paper_search_url, params=p)
    js = r.json()
    offset = js["next"]
    p["offset"] = offset
    papers = js["data"]
    return papers, p


def search_all(keyword, lim=100):
    all_papers = []
    p = main_param.copy()
    p["query"] = keyword
    while lim > 0:
        lim -= int(p["limit"])
        papers, p = search(keyword, p=p)
        if len(papers):
            all_papers.extend(papers)
        else:
            break
    return all_papers


def search_all_keywords(keywords, lim=100):
    all_papers = []
    for keyword in keywords:
        papers = search_all(keyword, lim=lim)
        all_papers.extend(papers)
    return all_papers


def search_author(author_id):
    if author_id in author_database:
        return author_database[author_id]
    url = author_detail_url(author_id)
    api_limit()
    r = requests.get(url, params=author_param)
    js = r.json()
    if len(js.keys()) < 3:
        return None
    pc = js["paperCount"]
    cc = js["citationCount"]
    hi = js["hIndex"]
    pch = f"{pc}-{cc}-{hi}"
    author_database[author_id] = pch
    return pch


if __name__ == "__main__":
    papers, _ = search("deep+learning")
