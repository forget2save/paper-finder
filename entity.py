class Paper:
    def __init__(self, title, authors, fields, abstract, abs_link, pdf_link) -> None:
        self.title = title
        self.authors = authors
        self.fields = fields
        self.abstract = abstract
        self.abs_link = abs_link
        self.pdf_link = pdf_link


class Author:
    def __init__(self, profile_link, affiliation, interest, citation) -> None:
        self.profile_link = profile_link
        self.affiliation = affiliation
        self.interest = interest
        self.citation = citation
