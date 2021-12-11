import os
from pickle import load
from typing import Dict, List, Any


def pickle_load(obj: Any, file: str):
    if not os.path.exists(file):
        data = obj
    else:
        with open(file, "rb") as f:
            data = load(f)
    return data


papers: List[Any]
papers = pickle_load(list(), "./papers/raw")
authorcites = pickle_load(dict(), "./papers/authors")
papers.sort(key=lambda x: x["citationCount"] + x["year"] * 100000, reverse=True)

year = 10000

with open("./summary.md", "w", encoding="utf-8") as f:
    for paper in papers:
        if paper["year"] and paper["year"] < year:
            year = paper["year"]
            f.write("# " + f"{year}\n\n")
        venue = paper["venue"]
        title = paper["title"]
        citation = paper["citationCount"]
        authors = paper["authors"]
        abstract = paper["abstract"]
        external_ids = paper["externalIds"]
        arxiv_id = external_ids["ArXiv"] if "ArXiv" in external_ids else None
        
        tmp = []
        for author in authors:
            if author["authorId"] is None:
                tmp.append(f"{author['name']}")
            elif author["authorId"] in authorcites:
                pch = authorcites[author["authorId"]]
                tmp.append(f"{author['name']}({pch})")
        authors = "; ".join(tmp)
        
        t = title.replace("?", ":").split(":")[0]
        
        f.write("## " + title + f"[{citation}]\n\n")
        f.write(authors + "\n\n")
        if venue:
            f.write(venue + "\n\n")
        if arxiv_id:
            f.write(f"[pdf available](./papers/{t}.pdf)\n\n")
        if abstract:
            f.write(abstract + "\n\n")

