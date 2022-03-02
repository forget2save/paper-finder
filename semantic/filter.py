import re
import os
from summary import Paper
from storage import pickle_load
from typing import List, Union


def unique_paper(papers: List[Paper]):
    result = []
    id_set = set()
    for paper in papers:
        if paper.paper_id not in id_set:
            id_set.add(paper.paper_id)
            result.append(paper)
    return result


def filter_by_unique_id(papers: List[Paper], folders: Union[str, List[str]]):
    if isinstance(folders, str):
        u = [os.path.join(folders, "UNIQUE")]
    else:
        u = [os.path.join(x, "UNIQUE") for x in folders]
    u = [pickle_load(set(), x) for x in u]
    result = []
    for paper in papers:
        flag = True
        for uni in u:
            if paper.paper_id in uni:
                flag = False
                break
        if flag:
            result.append(paper)
    return result


def filter_low_citation(papers: List[Paper], citation: int, older: int):
    result = []
    for paper in papers:
        if paper.citation < citation and paper.year <= older:
            pass
        else:
            result.append(paper)
    return result


def filter_years(papers: List[Paper], start: int, end: int):
    result = []
    for paper in papers:
        if start <= paper.year <= end:
            result.append(paper)
    return result


def filter_title_by_words(papers: List[Paper], ban_words: List[str]):
    bans = [re.compile(x) for x in ban_words]
    result = []
    for paper in papers:
        text = paper.title.lower()
        flag = False
        for ban in bans:
            if ban.findall(text):
                flag = True
                break
        if not flag:
            result.append(paper)
    return result


def filter_abstract_by_words(papers: List[Paper], ban_words: List[str]):
    bans = [re.compile(x) for x in ban_words]
    result = []
    for paper in papers:
        if not paper.abstract:
            continue
        text = paper.abstract.lower()
        flag = False
        for ban in bans:
            if ban.findall(text):
                flag = True
                break
        if not flag:
            result.append(paper)
    return result


def filter_citation_per_year(papers: List[Paper], speed:int):
    from datetime import datetime
    result = []
    for paper in papers:
        lb = int(max(0.5, int(datetime.now().year) - paper.year) * speed)
        if paper.citation >= lb:
            result.append(paper)
    return result
