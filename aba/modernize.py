import argparse
from .strings.modern import modernize_sentence
from .strings.utils import cacc, wacc

def run():
	
	modern_dic_path = 'data/dic_morphalou.tsv'
	learn_dic_path 	= 'data/dic_p17.tsv'

	parser = argparse.ArgumentParser()
	parser.add_argument('text_old_path', type = str,
		help = 'path to the original text')
	parser.add_argument('-n', '--text_new_path', type = str,
		help = 'path to the modernized text for evaluation')
	args = parser.parse_args()

	# output
	text_mod_path = 'result/' + '.'.join(args.text_old_path.split('/')[-1].split('.')[0:-1]) + '_mod_aba.txt'

	# read files
	text_old	= [line.strip() for line in open(args.text_old_path, 'r', encoding = 'utf8')]
	modern_dic 	= {line.strip() for line in open(modern_dic_path, 'r', encoding = 'utf8')}
	learn_dic 	= {old:new for (old, new, _) in [l.split('\t') for l in open(learn_dic_path, 'r', encoding = 'utf8')]}

	# modernize
	print(f'translating {args.text_old_path}')
	text_mod 	= [modernize_sentence(s, modern_dic, learn_dic) for s in text_old]

	# save modernized text
	print(f'saving to {text_mod_path}')
	open(text_mod_path, 'w', encoding = 'utf8').write('\n'.join(text_mod))
	
	# compare with new text
	if args.text_new_path:
		print(f'comparing to {args.text_new_path}')
		text_new 	= [line.strip() for line in open(args.text_new_path, 'r', encoding = 'utf8')]
		result_aba 	= [(mod, new) for (mod, new) in zip(text_mod, text_new)]
		result_base = [(old, new) for (old, new) in zip(text_old, text_new)]
		# print evaluation
		print(
			f'base :\n'
			f'cacc = {cacc(result_base) * 100}\n'
			f'wacc = {wacc(result_base) * 100}'
		)
		print(
			f'aba :\n'
			f'cacc = {cacc(result_aba) * 100}\n'
			f'wacc = {wacc(result_aba) * 100}'
		)

if __name__ == '__main__':
	run()