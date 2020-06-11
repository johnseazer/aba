# FREN
Français de la Renaissance

Approches automatiques de modernisation de textes du XVIe au XVIIIe siècle

## Download PARALLEL17

* Install `pygit2`

```python
pip install pygit2
```

* Run `dl_parallel17.py`

```
python dl_parallel17.py
```

## Align Words

Read directory containing `.tsv` files aligned on sentences and create a new directory with the same files aligned on words.

* Run `tsv_align_words.py` 

```bash
python tsv_align_words.py
```

## Extract Dictionary

Read directory containing `.tsv` files aligned on words and create dictionary of all encountered pairs with count.

* Run `tsv_extract_dict.py`

```bash
python tsv_extract_dict.py
```

## Label Dictionary

Read `.tsv` dictionary from `tsv_extract_dic.py` and create dictionary with same entries and rules applied in translation

* Run `tsv_label_dict.py`

```bash
python tsv_label_dict.py
```
