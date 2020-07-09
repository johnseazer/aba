def init_submat_chars():
	submat = {}
	# diacritics
	add_to_submat('a', 'à', 2, submat)
	add_to_submat('a', 'â', 2, submat)
	add_to_submat('â', 'a', 2, submat)
	add_to_submat('ã', 'a', 2, submat)
	add_to_submat('c', 'ç', 2, submat)
	add_to_submat('e', 'é', 2, submat)
	add_to_submat('e', 'è', 2, submat)
	add_to_submat('e', 'ê', 2, submat)
	add_to_submat('é', 'e', 2, submat)
	add_to_submat('ë', 'e', 2, submat)
	add_to_submat('ẽ', 'e', 2, submat)
	add_to_submat('i', 'î', 2, submat)
	add_to_submat('o', 'ô', 2, submat)
	add_to_submat('õ', 'o', 2, submat)
	add_to_submat('u', 'û', 2, submat)
	add_to_submat('û', 'u', 2, submat)
	add_to_submat('ü', 'u', 2, submat)
	add_to_submat('ũ', 'u', 2, submat)
	# ramist
	add_to_submat('i', 'j', 2, submat)
	add_to_submat('j', 'i', 1, submat)
	add_to_submat('u', 'v', 1, submat)
	add_to_submat('v', 'u', 1, submat)
	# replacement
	add_to_submat('c', 'q', 1, submat)
	add_to_submat('q', 'c', 1, submat)
	add_to_submat('g', 'n', 1, submat)
	add_to_submat('n', 'm', 1, submat)
	add_to_submat('s', 'z', 1, submat)
	add_to_submat('y', 'i', 2, submat)
	add_to_submat('œ', 'o', 2, submat)
	add_to_submat('o', 'œ', 2, submat)
	# old chars
	add_to_submat('&', 'e', 2, submat)
	add_to_submat('ß', 's', 2, submat)
	add_to_submat('ſ', 's', 2, submat)
	add_to_submat('ſ', 'z', 1, submat)
	return submat

def init_submat_words():
	submat = {}
	add_to_submat('&', 'et', 4, submat)
	return submat

def add_to_submat(a, b, n, submat):
    if a not in submat:
        submat[a] = {b: n}
    else:
        submat[a].update({b: n})