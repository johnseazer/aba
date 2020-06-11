# !pip install pygit2

from os.path import exists
from shutil import rmtree
from pygit2 import clone_repository

# source
repo_url = 'https://github.com/e-ditiones/PARALLEL17.git'
repo_dir = 'PARALLEL17'

if exists(repo_dir):
	print('parallel17 directory already exists')
	print('delete it if you want to download parallel17 again')	
	# print('> deleting previous version...')
	# rmtree(repo_dir)
	# print('> deleted')
	
else :
	print('downloading parallel17...')
	clone_repository(repo_url, repo_dir)
	print('downloaded')