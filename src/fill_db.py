from site_rank.lib.rank.db_connection import RankDBHandler
from site_rank.lib.rank.site_crawler import SiteCrawler
from site_rank.lib.rank.nltk_wrapper import NltkWrapper

#Init handler for DB.
db_handler = RankDBHandler()

#Querry site list from DB.
sites = db_handler.get_site_list()

#Init basic site crawler.
crawler = SiteCrawler()

#Init NLTK package wrapper.
nltk = NltkWrapper()

#Iterate all sites in database.
for site in sites:
    #Remove trailing spaces.
    site = site.strip()
    try:
        text = crawler.crawl(site)
    except:
        text = ''
    #Convert site text to tokenized word list without stopwords.
    words = nltk.get_sanitized_word_list(text)
    
    #querry the site id.
    site_id = db_handler.get_site_id(site)
    
    #Update containment data in database.
    for word in words:
        db_handler.update_containment(site_id, db_handler.add_word(word)) 

