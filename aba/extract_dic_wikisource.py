# Script to extract *old french → modern french* dictionary from Wikisource

from bs4 import BeautifulSoup
import urllib.request
import os, re

# destination file
dst_path = os.path.join('data','dic_wikisource.tsv')

# base url
url_root = 'https://fr.wikisource.org'
url_path = '/wiki/Wikisource:Dictionnaire'

print(f'Extracting wikisource dictionary to {dst_path}')

# get base html page
html_page = urllib.request.urlopen(url_root + url_path)
# parse base html page
parsed_page = BeautifulSoup(html_page, 'html.parser')

# find relevant links : relative urls starting like url_path + '/'
links = [url_root + link.get('href') for link in parsed_page.findAll('a', attrs = {'href': re.compile('^' + url_path + '/')})]

# open destination file
dst_file = open(dst_path, 'w', encoding = 'utf8')

# process links
for link in links:
	# get html page
	html_page = urllib.request.urlopen(link)
	# parse html page
	parsed_page = BeautifulSoup(html_page, 'html.parser')
	# find dict content
	content = parsed_page.find('div', attrs = {'class': u'mw-parser-output'})
	# find list elements
	for list_element in content.findAll('li'):
		# get entry
		entry = list_element.get_text()
		# parse entry to tsv
		entry = entry.replace(': ', '\t')
		entry = entry.replace('\xa0:', '\t')
		entry = entry.replace(':', '\t')
		if len(entry.rstrip().split('\t')) != 2:
			continue
		# write entry to destination file
		dst_file.write(entry + '\n')

dst_file.close()

print('Done.')