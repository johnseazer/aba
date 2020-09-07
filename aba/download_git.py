from pathlib import Path
from pygit2 import clone_repository

def run():

	repo_url = 'https://github.com/PhilippeGambette/PARALLEL17.git'

	# set download path
	dl_path = Path('download').mkdir(parents = True, exist_ok = True)

	# get repository name and set repository path
	repo_name = repo_url.split('/')[-1].split('.')[0]
	repo_path = dl_path / repo_name

	if repo_path.exists():
		print(f'{repo_path} already exists. Please delete before downloading again.')
		return

	# download repository
	print(f'Downloading {repo_name} from {repo_url}...')
	clone_repository(repo_url, repo_path)
	print(f'{repo_name} downloaded to {repo_path}')

if __name__ == '__main__':
	run()