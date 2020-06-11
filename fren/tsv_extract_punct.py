'''
download source
'''

#!pip install pygit2

from shutil import rmtree
from os.path import exists
from pygit2 import clone_repository

# source
repo_url = 'https://github.com/e-ditiones/PARALLEL17.git'
repo_dir = 'PARALLEL17'

# delete repository directory if needed
# rmtree(repo_dir)

# clone repository
if not exists(repo_dir):
	clone_repository(repo_url, repo_dir)

'''
extract punctuation
'''

from os import listdir
from os.path import isfile, join

# source directory
src_dir = "PARALLEL17/corpus_tsv"

# source files
files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]

# init result
punct = []

# process files
for f in files:
	# open file
	srcf = open(src_dir + '/' + f, 'r', encoding = 'utf8')
	# process lines
	for line in srcf.readlines():
		# process chars
		for char in line:
			code = ord(char)
			if ((code < ord('a') or code > ord('z')) and
				(code < ord('A') or code > ord('Z')) and
				char not in ' \t\n&0123456789ÀÂÆÇÈÉÊÎÔßàâãæçèéêëîïñôõùúûüĩōŒœũſέαδεηθικλμνοπρςστϖẽὶὸῖῶ'):
				# add punctuation to the list
				if char not in punct:
					punct.append(char)

# sort in unicode order
punct.sort()
# print as a list to see non-printing chars
print('list :')
print(punct)
# print as a string for use
print('string :')
print(''.join(punct))