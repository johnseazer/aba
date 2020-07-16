# script to extract dict from morphalou
# link : `https://www.ortolang.fr/market/lexicons/morphalou`
# path : `morphalou/4/Morphalou3.1_formatCSV_toutEnUn/Morphalou3.1_CSV.csv`

filename = 'data/Morphalou3.1_CSV.csv'
dictname = 'data/dic_morphalou.tsv'

print('extracting morphalou dictionary')

with open(filename, 'r', encoding = 'utf8') as f:
	dic = [line.split(';')[9] for line_no, line in enumerate(f.readlines(), start = 1) if line_no >= 17 ]

with open(dictname, 'w', encoding = 'utf8') as f:
	for word in dic:
		f.write(f'{word}\n')

print(f'morphalou dictionary extracted to {dictname}')