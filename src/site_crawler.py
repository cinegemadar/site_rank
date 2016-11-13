from lxml import html
import requests

page = requests.get('http://Kidshealth.org/en/teens/')

tree = html.fromstring(page.content)

content = tree.xpath('//b/text()')

print('\n'.join(content))