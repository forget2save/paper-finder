import os
from collections import defaultdict
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


paper_database = pickle_load(defaultdict(dict), "./PAPERS")
author_database = pickle_load(defaultdict(str), "./AUTHORS")


def renew_papers(papers):
    for paper in papers:
        pid = paper["paperId"]
        paper_database[pid] = paper


def dump_database():
    pickle_dump(paper_database, "./PAPERS")
    pickle_dump(author_database, "./AUTHORS")
