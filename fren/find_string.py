from pathlib import Path

string = "paroiſſoient par"

download = Path('download')
input_dir = download/'PARALLEL17'/'corpus_tsv'

# get input files
files = [f.name for f in input_dir.iterdir() if f.is_file() and f.suffix == '.tsv']

# process files
for f in files:
	# get lines from source
	with open(input_dir / f, 'r', encoding = 'utf8') as src:
		lines = src.readlines()
	for line_no, line in enumerate(lines):
		if string in line:
			print(f'## {f}\n* {line_no + 1}\n```\n{line}```')