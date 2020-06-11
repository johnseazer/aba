# !pip install bs4

from bs4 import BeautifulSoup
import urllib
import re

# destination file
dst_name = 'wikisource_dict.tsv'

# base url
url_root = 'https://fr.wikisource.org'
url_path = '/wiki/Wikisource:Dictionnaire'

# get base html page
html_page = urllib.request.urlopen(url_root + url_path)
# parse base html page
parsed_page = BeautifulSoup(html_page, 'html.parser')

# find relevant links : relative urls starting like url_path + '/'
links = []
for link in parsed_page.findAll('a', attrs={'href': re.compile('^' + url_path + '/')}):
    links.append(url_root + link.get('href'))

# open destination file
dst_file = open(dst_name, 'w', encoding = 'utf8')

# process links
for link in links:
    # get html page
    html_page = urllib.request.urlopen(link)
    # parse html page
    parsed_page = BeautifulSoup(html_page, 'html.parser')
    # find dict content
    content = parsed_page.find('div', attrs={'class': u'mw-parser-output'})
    # find list elements
    for list_element in content.findAll('li'):
        # get entry
        entry = list_element.get_text()
        # parse entry to tsv
        entry = entry.replace(': ', '\t')
        # write entry to destination file
        dst_file.write(entry + '\n')

dst_file.close()