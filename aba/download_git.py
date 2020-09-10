import argparse
from pathlib import Path
from pygit2 import clone_repository

def run():

	default_repo_url = 'https://github.com/PhilippeGambette/PARALLEL17.git'
	
	parser = argparse.ArgumentParser()
	parser.add_argument('repo_url', type = str,
		help = 'url to the git', 
		default = default_repo_url)
	args = parser.parse_args()

	# set download path
	dl_path = Path('download')

	# init download folder
	dl_path.mkdir(parents = True, exist_ok = True)

	# get repository name and set repository path
	repo_name = args.repo_url.split('/')[-1].split('.')[0]
	repo_path = dl_path / repo_name

	if repo_path.exists():
		print(f'Folder {repo_path} already exists. Please delete folder before downloading again.')
		return

	# download repository
	print(f'Downloading {repo_name} to {repo_path}...')
	clone_repository(args.repo_url, repo_path)
	print(f'Done.')

if __name__ == '__main__':
	run()