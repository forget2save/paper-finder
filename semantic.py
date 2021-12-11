import requests
import os
import time
from pickle import dump, load
from typing import Dict, List, Any


def pickle_load(obj: Any, file: str):
    if not os.path.exists(file):
        data = obj
    else:
        with open(file, "rb") as f:
            data = load(f)
    return data

def pickle_dump(obj: Any, file: str):
    with open(file, "wb") as f:
        dump(obj, f)

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
arxiv_pdf_url = lambda arxiv_id: "/".join([arxiv_url, "pdf", arxiv_id])

param = {
    "query": "adversarial+attack+physical",
    "fields": "title,venue,year,fieldsOfStudy,abstract,externalIds,citationCount,authors",
    "limit": "100",
    "offset": "0",
}

param2 = {
    "fields": "paperCount,citationCount,hIndex",
}

js: dict
papers: List[Dict[str, Any]]

downloaded = pickle_load(set([]), "./papers/downloaded")
authorcites = pickle_load(dict(), "./papers/authors")
all_papers = []

try:
    while True:
        r = requests.get(paper_search_url, proxies=proxy, params=param)
        js = r.json()
        offset = js["next"]
        param["offset"] = offset
        papers = js["data"]
        all_papers.extend(papers)
        num = len(papers)
        print(offset, num)
        if num == 0:
            break
        for paper in papers:
            paper_id = paper["paperId"]
            title = paper["title"]
            citation = paper["citationCount"]
            authors = paper["authors"]
            abstract = paper["abstract"]
            external_ids = paper["externalIds"]
            arxiv_id = external_ids["ArXiv"] if "ArXiv" in external_ids else None
            
            # if paper_id in downloaded:
            #     continue
            
            # tmp = []
            # for author in authors:
            #     if author["authorId"] is None:
            #         tmp.append(f"{author['name']}")
            #     elif author["authorId"] in authorcites:
            #         print("find an author")
            #         pch = authorcites[author["authorId"]]
            #         tmp.append(f"{author['name']}({pch})")
            #     else:
            #         print("fetch from web")
            #         time.sleep(0.5)
            #         url = author_detail_url(author["authorId"])
            #         r2 = requests.get(url, proxies=proxy, params=param2)
            #         js2 = r2.json()
            #         if len(js2.keys()) < 3:
            #             tmp.append(f"{author['name']}")
            #         else:
            #             pc = js2["paperCount"]
            #             cc = js2["citationCount"]
            #             hi = js2["hIndex"]
            #             pch = f"{pc}-{cc}-{hi}"
            #             authorcites[author["authorId"]] = pch
            #             tmp.append(f"{author['name']}({pch})")
            # authors = ";".join(tmp)

            # with open("./papers/summary.md", "a", encoding="utf-8") as f:
            #     f.write("## " + title + f"[{citation}]\n\n")
            #     f.write(authors + "\n\n")
            #     if abstract is not None:
            #         f.write("### Abstract\n\n" + abstract + "\n\n")
            
            if arxiv_id and (citation >= 10 or "2" == arxiv_id[0]):
                t = title.replace("?", ":").split(":")[0]
                print(t)
                fp = f"./papers/{t}.pdf"
                if not os.path.exists(fp):
                    print(arxiv_id, citation, title)
                    r_d = requests.get(arxiv_pdf_url(arxiv_id), stream=True)
                    with open(fp, "wb") as f:
                        f.write(r_d.content)
            # downloaded.add(paper["paperId"])
            
except Exception as e:
    print(e)
    print(js2)
finally:
    pickle_dump(all_papers, "./papers/raw")
    pickle_dump(downloaded, "./papers/downloaded")
    pickle_dump(authorcites, "./papers/authors")
