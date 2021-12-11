import re
from summary import Paper
from typing import List


def filter_low_citation(papers: List[Paper], citation: int, older: int):
    result = []
    for p in papers:
        if p.citation < citation and p.year <= older:
            pass
        else:
            result.append(p)
    return result


def filter_years(papers: List[Paper], start: int, end: int):
    result = []
    for p in papers:
        if start <= p.year <= end:
            result.append(p)
    return result


def filter_title_by_words(papers: List[Paper], ban_words: List[str]):
    bans = [re.compile(x) for x in ban_words]
    result = []
    for p in papers:
        text = p.title.lower()
        flag = False
        for ban in bans:
            if ban.findall(text):
                flag = True
                break
        if not flag:
            result.append(p)
    return result


def filter_abstract_by_words(papers: List[Paper], ban_words: List[str]):
    bans = [re.compile(x) for x in ban_words]
    result = []
    for p in papers:
        if not p.abstract:
            continue
        text = p.abstract.lower()
        flag = False
        for ban in bans:
            if ban.findall(text):
                flag = True
                break
        if not flag:
            result.append(p)
    return result
