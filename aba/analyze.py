import argparse, os

from .utils.saving import extract_dic
from .utils.modern import label_dic

def run():

	default_src_dir = os.path.join('data','PARALLEL17_words')
	default_raw_dic_path = os.path.join('data','dic_p17.tsv')
	default_lab_dic_path = os.path.join('data','dic_p17_labeled.tsv')

	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--src_dir', type = str,
		help = 'source directory for .dic files',
		default = default_src_dir)
	parser.add_argument('-r', '--raw_dic_path', type = str,
		help = 'filename for dictionary file',
		default = default_raw_dic_path)
	parser.add_argument('-l', '--lab_dic_path', type = str,
		help = 'filename for dictionary file',
		default = default_lab_dic_path)

	args = parser.parse_args()

	# analyze corpus
	extract_dic(args.src_dir, args.raw_dic_path)
	label_dic(args.raw_dic_path, args.lab_dic_path)


if __name__ == '__main__':
	run()