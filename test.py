from fren.strings.alignment import needleman_wunsch
from fren.strings.distance import levenshtein
from fren.strings.substitution import init_submat_chars
from fren.strings.nlptools import preprocess, align_compound_words

a = "en ſuite dequoy il continua de chercher comme les autres, mais ils chercherent tous inutilement."
b = "ensuite de quoi il continua de chercher comme les autres, mais ils cherchèrent tous inutilement."

a = preprocess(a)
b = preprocess(b)

(a, b) = needleman_wunsch(a, b, submat = init_submat_chars(), mode = 'words')

print('---')
for (s, t) in zip(a, b):
	print(s, t)
print('---')
(a, b) = align_compound_words(a, b)
for (s, t) in zip(a, b):
	print(s, t)