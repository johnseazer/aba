import argparse
import os

from .utils.modern import modernize_sentence

def run():
	
	modern_dic_path = os.path.join('data','dic_morphalou.tsv')
	learn_dic_path 	= os.path.join('data','dic_p17.tsv')
	name_dic_path 	= os.path.join('data','dic_resources.txt')

	parser = argparse.ArgumentParser()
	parser.add_argument('text_old_path', type = str,
		help = 'path to the original text')
	args = parser.parse_args()

	# output
	if os.path.isdir('result') == False:
	   os.mkdir("result")
	text_mod_path = os.path.join('result','.'.join(os.path.basename(args.text_old_path).split('.')[0:-1]) + '_mod_aba.txt')

	# read files
	text_old	= [line.strip() for line in open(args.text_old_path, 'r', encoding = 'utf8')]
	modern_dic 	= {line.strip() for line in open(modern_dic_path, 'r', encoding = 'utf8')}
	name_dic 	= {line.strip() for line in open(name_dic_path, 'r', encoding = 'utf8')}
	learn_dic 	= {old:new for (old, new, _) in [l.split('\t') for l in open(learn_dic_path, 'r', encoding = 'utf8')]}

	# modernize
	print(f'translating {args.text_old_path}')
	text_mod 	= [modernize_sentence(s, modern_dic, learn_dic, name_dic = name_dic) for s in text_old]

	# save modernized text
	print(f'saving to {text_mod_path}')
	open(text_mod_path, 'w', encoding = 'utf8').write('\n'.join(text_mod))
	

if __name__ == '__main__':
	run()