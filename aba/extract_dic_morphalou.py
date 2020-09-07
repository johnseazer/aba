# script to extract dict from morphalou
# download morphalou from `https://www.ortolang.fr/market/lexicons/morphalou`
# extract and get `morphalou/4/Morphalou3.1_formatCSV_toutEnUn/Morphalou3.1_CSV.csv`
# move `Morphalou3.1_CSV.csv` to `download/`

filename = 'download/Morphalou3.1_CSV.csv'
dictname = 'data/dic_morphalou.tsv'

print('Extracting Morphalou dictionary...')

with open(filename, 'r', encoding = 'utf8') as f:
	# entries start at line 17, word is in column 9
	dic = [line.split(';')[9] for line_no, line in enumerate(f.readlines(), start = 1) if line_no >= 17 ]

with open(dictname, 'w', encoding = 'utf8') as f:
	for word in dic:
		f.write(f'{word}\n')

print(f'Morphalou dictionary extracted to {dictname}')