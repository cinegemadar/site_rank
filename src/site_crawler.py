from lxml import html
import requests
import logging
import itertools 
import string

logging.basicConfig(level=logging.INFO)
gLogger = logging.getLogger('SITERank') 

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
        return [self.remove_special_cahrs(x) for x in self.mWords if len(x)>limit]


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

        #Parse all text blocks.
        text_list = self.mTree.xpath('//body//*[not(self::script)]/text()')
        
        #Create word list from text blocks.
        word_list = [x.split() for x in text_list]
        
        #Merge list of list words to list of words.
        self.mWords = list(itertools.chain.from_iterable(word_list))

    def remove_special_cahrs(self, s):
        #return ''.join([x for x in s.strip() if x.isalnum()])
        return s.strip().strip(string.punctuation)

'''
'''
#TEST RUN
c = SiteCrawler()
r = c.crawl('cnn.com')
with open('c:\\Source\\site_rank\\raw_data\\test_cnn_data.txt', 'w') as of:
    for w in r:
        
        try:
            of.write(w + '\n')
        except UnicodeEncodeError:
            gLogger.error("Encoding error, skip {}".format(w.encode('utf-8')))

        