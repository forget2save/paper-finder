import os
from collections import defaultdict
from pickle import dump, load
from typing import Dict, List, Any
from config import DATABASE


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


if not os.path.exists(DATABASE):
    print("Set your path to database!")
    exit(1)
PAPERS = pickle_load(defaultdict(dict), os.path.join(DATABASE, "PAPERS"))
AUTHORS = pickle_load(defaultdict(str), os.path.join(DATABASE, "AUTHORS"))


def renew_papers(papers):
    for paper in papers:
        pid = paper["paperId"]
        PAPERS[pid] = paper


def dump_database():
    pickle_dump(PAPERS, os.path.join(DATABASE, "PAPERS"))
    pickle_dump(AUTHORS, os.path.join(DATABASE, "AUTHORS"))
