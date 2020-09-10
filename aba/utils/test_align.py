from aba.utils.strings import needleman_wunsch, levenshtein, add_to_submat, init_matrix

def test_init_matrix():
	a = 'a'
	b = 'bb'
	res = (2, 3, [[0, 4, 8], [4, 0, 0]])
	factor = 4
	assert init_matrix(a, b, factor) == res

def test_levensthein():
	a = 'abc'
	b = 'xyz'
	res = 6
	costs = (1, 1, 2)
	assert levenshtein(a, b, costs) == res

def test_needleman_wunsch():
	submat = {}
	add_to_submat('é', 'e', 2, submat)
	a = 'cét'
	b = 'cette'
	align = (['c', 'é', '¤', 't', '¤'], ['c', 'e', 't', 't', 'e'])
	assert needleman_wunsch(a, b, submat = submat) == align