import traceback
from storage import renew_papers, dump_database
from search import search_all_keywords
from summary import Paper, new_summary, write_summary, sort_paper, write_unique_ids
from filter import unique_paper, filter_abstract_by_words, filter_title_by_words, filter_years, filter_low_citation

save_path = "./new-survey"
keywords = ["physical+adversarial+attack"]
ban_words = ["cps", "gan"]

try:
    new_summary(save_path)
    papers = search_all_keywords(keywords, lim=100)
    renew_papers(papers)
    papers = unique_paper([Paper(p) for p in papers])
    print("Find", len(papers))
    papers = filter_years(papers, 2016, 2021)
    print("In year range", len(papers))
    papers = filter_low_citation(papers, 1, 2021)
    papers = filter_low_citation(papers, 10, 2020)
    papers = filter_low_citation(papers, 20, 2019)
    papers = filter_low_citation(papers, 30, 2018)
    papers = filter_low_citation(papers, 40, 2017)
    papers = filter_low_citation(papers, 50, 2016)
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
