from site_rank.lib.rank.db_connection import RankDBHandler
from site_rank.lib.rank.site_crawler import SiteCrawler
from site_rank.lib.rank.nltk_wrapper import NltkWrapper

#Init handler for DB.
db_handler = RankDBHandler()

#Querry site list from DB.
sites = db_handler.get_site_list()

crawler = SiteCrawler()
nltk = NltkWrapper()

for site in sites[:100]:
    site = site.strip()
    try:
        text = crawler.crawl(site)
    except:
        text = ''
    words = nltk.get_sanitized_word_list(text)
    site_id = db_handler.get_site_id(site)
    for word in words:
        db_handler.update_containment(site_id, db_handler.add_word(word)) 

