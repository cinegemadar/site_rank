from lxml import html
from site_rank_global import logger
import requests

class SiteCrawler():
    '''
    Simple website text crawler.
    '''

    def crawl(self, site, lang=''):

        self.site = site

        try:
            self.load_site()
        except requests.exceptions.MissingSchema:
            logger.warning('Missing schema')
            self.site = 'http://' + self.site 
            self.load_site()
        except requests.exceptions.ConnectionError:
            logger.error('Cannot open {}'.format(self.site))
            return ''

        try:
            self.build_structure()
        except UnicodeDecodeError:
            logger.error('{} site is Unicode encoded. We currently support UTF-8 Only. Skipping this site for now.'.format(self.site))
            return ''

        return ' '.join(self.site_text)

    def load_site(self):
        
        logger.info('Loading {}'.format(self.site))
        self.page = requests.get(self.site)
        


    def build_structure(self):
        
        
        
        #Build HTML structure.
        self.tree = html.fromstring(self.page.content.decode('utf-8'))
        #Parse text data from site.
        self.site_text = self.tree.xpath('//body//*[not(self::script)]/text()')
        
        
        
'''TEST
from nltk_wrapper import NltkWrapper

crawler = SiteCrawler()
nltk = NltkWrapper()
words = crawler.crawl('google.com')
s_words = nltk.get_sanitized_word_list(words)
print(s_words)
'''