# Script to extract modern french dictionary from Morphalou
# 1. Download [Morphalou](https://www.ortolang.fr/market/lexicons/morphalou)
# 2. Copy `morphalou/4/Morphalou3.1_formatCSV_toutEnUn/Morphalou3.1_CSV.csv` to `download` folder
# 3. Run script
import os

src = os.path.join('download','Morphalou3.1_CSV.csv')
dst = os.path.join('data','dic_morphalou.tsv')

print(f'Extracting Morphalou dictionary to {dst}...')

# extract dic from morphalou
# entries start at line 17, word is in column 9
dic = [line.split(';')[9] for line_no, line in enumerate(open(src, 'r', encoding = 'utf8'), start = 1) if line_no >= 17]

# save dic
open(dst, 'w', encoding = 'utf8').write('\n'.join(dic))

print('Done.')