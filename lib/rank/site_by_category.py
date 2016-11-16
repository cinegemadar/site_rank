from __future__ import division  # Needed for forced floating point division.
from lxml import html
import requests


'''

Download RANK data from
http://www.alexa.com/topsites/global;SITENO
where 0 <= SITENO < MAX_PAGE
'''


def get_site_categories():
    '''
    Parse all available categories from alexa.
    '''

    page = requests.get('http://www.alexa.com/topsites/category')

    # tree = html.parse('c:\\dev\\web_rank\\alexa_category.html')
    tree = html.fromstring(page.content)

    categories = tree.xpath('//ul[@class="subcategories span3"]/li/a/text()')

    return categories


def get_sites(url):
    '''
    Parse site list from provided url.
    '''

    page = requests.get(url)
    tree = html.fromstring(page.content)
    sites = tree.xpath(
        '//ul/li[@class="site-listing"]' +
        '/div[@class="desc-container"]/p/a/text()'
    )

    return sites


categories = get_site_categories()

page_no = 3

base_url = 'http://www.alexa.com/topsites/category;{}/Top'.format(page_no)

site_repo = {}

for category in categories:
    best_sites = get_sites('{}/{}'.format(base_url, category))
    for site in best_sites:
        site_repo[site] = category

with open('sites_{}.csv'.format(page_no), 'w') as fp:
    for key in site_repo:
        fp.write('{}  ,  {}\n'.format(key, site_repo[key]))
