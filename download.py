import os
import requests

arxiv_url = "https://arxiv.org"
arxiv_pdf_url = lambda arxiv_id: "/".join([arxiv_url, "pdf", arxiv_id])


def download_arxiv(arxiv_id, save_path, rename=None):
    filename = rename + ".pdf" if rename else arxiv_id + ".pdf"
    filename = os.path.join(save_path, filename)
    if not os.path.exists(filename):
        print("Downloading from arxiv.")
        r_d = requests.get(arxiv_pdf_url(arxiv_id), stream=True)
        with open(filename, "wb") as f:
            f.write(r_d.content)
    else:
        print("File has existed!")


if __name__ == "__main__":
    download_arxiv("2109.13916", "./test")
