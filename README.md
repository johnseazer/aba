# FREN
Français de la Renaissance

Approches automatiques de modernisation de textes du XVIe au XVIIIe siècle

## Align Words

* Downloads the PARALLEL17 corpus
* Aligns words instead of sentences using Needleman-Wunsch
* Writes results to `corpus_tsv_aligned` directory as .tsv files

Install pygit2

```python
pip install pygit2
```

Results can either include all words or only words which are different between fren and fr

```python
# write differences only
delta_only = True
```

```python
# write everything
delta_only = False
```

Run the script

```bash
python align_words.py
```

