from lxml import html
import requests
import logging
import itertools 

logging.basicConfig(level=logging.INFO)
gLogger = logging.getLogger(__name__) 

class SiteCrawler():
    '''
    This class is a simple site crawler. Downloads all text data from given page.
    '''
    # def __init__(self):
    #     return

    
    def crawl(self, site='', limit=3):
        '''
        Crawl text from site.
        '''

        self.mSite = site

        self.load_page()

        self.parse_text()

        #Sanitize short entries from word list.
        return [x.strip() for x in self.mWords if len(x)>limit]


    def load_page(self):
        '''
        Load site to being processed.
        '''

        try:
            try:
                gLogger.info('Connecting to {}'.format(self.mSite))
                self.mPage =  requests.get(self.mSite)
            
            except requests.exceptions.MissingSchema:
                
                url_with_schema = '{}://{}'.format('http',self.mSite)

                gLogger.warning('Missing schema, trying {}'.format(url_with_schema))
                self.mPage =  requests.get(url_with_schema)

        except requests.exceptions.ConnectionError:
            gLogger.error('Cannot connect, skip {}'.format(self.mSite))

        self.mTree = html.fromstring(self.mPage.content)

    def parse_text(self):
        '''
        Parse text data from site.
        '''

        gLogger.info('Start parsing text from {}'.format(self.mSite))
        word_list = [x.split() for x in self.mTree.xpath('//body//*[not(self::script)]/text()')]
        self.mWords = list(itertools.chain.from_iterable(word_list))


c = SiteCrawler()
r = c.crawl('http://www.lipsum.com/feed/html')
with open('c:\\Source\\site_rank\\raw_data\\test_data.txt', 'w') as of:
    for w in r:
        
        try:
            of.write(w + '\n')
        except UnicodeEncodeError:
            gLogger.error("Encoding error, skip {}".format(w.encode('utf-8')))

        