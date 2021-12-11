import re
from summary import Paper
from typing import List


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
