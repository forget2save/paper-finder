import os
from search import search_author, download_arxiv
from typing import IO, Dict, Any, List
from storage import pickle_dump


class Paper:
    def __init__(self, d: Dict[str, Any]) -> None:
        self.paper_id = d["paperId"]
        self.title = d["title"]
        self.venue = d["venue"]
        self.year = d["year"] if d["year"] else 0
        self.fields = d["fieldsOfStudy"]
        self.citation = d["citationCount"]
        self.authors = d["authors"]
        self.abstract = d["abstract"]
        self.ext_ids = d["externalIds"]
        self.authors_text = None
        self.arxiv = self.ext_ids["ArXiv"] if "ArXiv" in self.ext_ids else None

    def get_authors(self) -> str:
        tmp = []
        for author in self.authors:
            if author["authorId"]:
                pch = search_author(author["authorId"])
                tmp.append(f"{author['name']}({pch})")
            else:
                tmp.append(author["name"])
        return "; ".join(tmp)

    def summary(self, f: IO):
        if not self.authors_text:
            self.authors_text = self.get_authors()
        f.write("## " + self.title + f"[{self.citation}]\n\n")
        f.write(self.authors_text + "\n\n")
        if self.venue:
            f.write(self.venue + "\n\n")
        if self.arxiv:
            f.write(f"[pdf available](./pdf/{self.arxiv}.pdf)\n\n")
        if self.abstract:
            f.write(self.abstract + "\n\n")


def sort_paper(papers: List[Paper]):
    papers = [(p.year, p.citation, p.title, p) for p in papers]
    papers.sort(reverse=True)
    papers = [p[3] for p in papers]
    return papers


def new_summary(save_path: str):
    filename = os.path.join(save_path, "summary.md")
    folder = os.path.join(save_path, "pdf")
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(filename, "w", encoding="utf-8") as f:
        pass


def write_info(save_path: str, paper: Paper):
    print("Writing summary.")
    filename = os.path.join(save_path, "summary.md")
    with open(filename, "a", encoding="utf-8") as f:
        paper.summary(f)


def write_summary(save_path: str, papers: List[Paper], download_pdf=False):
    filename = os.path.join(save_path, "summary.md")
    year = 1000000
    length = len(papers)
    for i, paper in enumerate(papers):
        print(i, "/", length)
        if paper.year < year:
            year = paper.year
            with open(filename, "a", encoding="utf-8") as f:
                f.write("# " + f"{year}\n\n")
        write_info(save_path, paper)
        if download_pdf and paper.arxiv:
            download_arxiv(paper.arxiv, save_path)


def write_unique_ids(save_path: str, papers: List[Paper]):
    filename = os.path.join(save_path, "UNIQUE")
    id_set = set()
    for paper in papers:
        id_set.add(paper.paper_id)
    pickle_dump(id_set, filename)
