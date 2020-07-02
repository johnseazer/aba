from fren.strings.alignment import needleman_wunsch
from fren.strings.distance import levenshtein
from fren.strings import substitution as sub
from fren.strings import utils

def test_init_matrix():
	a = 'a'
	b = 'bb'
	factor = 4
	res = (2, 3, [[0, 4, 8], [4, 0, 0]])
	assert utils.init_matrix(a, b, factor) == res

def test_levensthein():
	a = 'abc'
	b = 'xyz'
	costs = (1, 1, 2)
	res = 6
	assert levenshtein(a, b, costs) == res

def test_needleman_wunsch():
	submat = {}
	sub.add_to_submat('é', 'e', 2, submat)
	a = 'cét'
	b = 'cette'
	align = (['c', 'é', '¤', 't', '¤'], ['c', 'e', 't', 't', 'e'])
	assert needleman_wunsch(a, b, submat = submat) == align