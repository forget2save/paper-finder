import traceback
from storage import renew_papers, dump_database
from search import search_all_keywords
from summary import Paper, new_summary, write_summary, unique_paper, sort_paper, write_unique_ids
from filter import filter_abstract_by_words, filter_title_by_words, filter_years, filter_low_citation

save_path = "./physical-adversarial-attacks"
keywords = [
    "physical+adversarial+attack",
    "real+world+adversarial+attack",
    "robust+adversarial+attack",
    "universal+adversarial+attack",
    "practical+adversarial+attack",
]
ban_words = [
    "cyber",
    "cps",
    "reinforcement",
    "GAN",
]

try:
    new_summary(save_path)
    papers = search_all_keywords(keywords, lim=200)
    renew_papers(papers)
    papers = unique_paper([Paper(p) for p in papers])
    print("Find", len(papers))
    papers = filter_years(papers, 2016, 2021)
    print("In year range", len(papers))
    papers = filter_low_citation(papers, 10, 2019)
    papers = filter_low_citation(papers, 20, 2018)
    print("After filtering low citation", len(papers))
    papers = filter_title_by_words(papers, ban_words)
    papers = filter_abstract_by_words(papers, ban_words)
    print("After filtering ban words", len(papers))
    papers = sort_paper(papers)
    write_summary(save_path, papers, download_pdf=True)
    write_unique_ids(save_path, papers)
except Exception as e:
    print(e)
    print(traceback.format_exc())
finally:
    dump_database()
