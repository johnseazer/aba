# FREN
Français de la Renaissance

Approches automatiques de modernisation de textes du XVIe au XVIIIe siècle

## Install

* With make

```bash
make
```

* Without make

```bash
pip install -r requirements.txt
```

## Generate Data

### Extract Wikisource Dictionary

```
python -m fren.extract_dic_wikisource
```

### Extract Morphalou Dictionary

* Get [Morphalou](https://www.ortolang.fr/market/lexicons/morphalou)

* Move `morphalou/4/Morphalou3.1_formatCSV_toutEnUn/Morphalou3.1_CSV.csv` to `data`
* Extract

```
python -m fren.extract_dic_morphalou
```

## Analyze Corpus

```
python -m fren.analyze
```

* Downloads [PARALLEL17](https://github.com/e-ditiones/PARALLEL17) corpus
* Aligns PARALLEL17 by words
* Creates corresponding dictionary with occurence count
* Completes dictionary with additional data

delete result folder before realigning corpus

## Modernize Corpus

```
python -m fren.modernize
```

## Run Tests

```bash
py.test
```