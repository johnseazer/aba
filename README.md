# ABA

Alignment-Based Approach for automatic modernization of abach texts from the 16th to the 18th century

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

### Download and Analyze PARALLEL17

* Manually or automatically download [PARALLEL17](https://github.com/e-ditiones/PARALLEL17) and put it into the `download` folder

```bash
python -m aba.download_git
python -m aba.analyze_corpus
```

* Aligns PARALLEL17 by words
* Creates two P17 dictionaries

### Extract Morphalou Dictionary

* Manually download [Morphalou](https://www.ortolang.fr/market/lexicons/morphalou)
* Copy `morphalou/4/Morphalou3.1_formatCSV_toutEnUn/Morphalou3.1_CSV.csv` to `download` folder
* Run script

```bash
python -m aba.extract_dic_morphalou
```

### Extract Wikisource Dictionary

```bash
python -m aba.extract_dic_wikisource
```

## Modernize Corpus

```bash
python -m aba.modernize_corpus
```

## Modernize Text

```bash
python -m aba.modernize [-h] [-n TEXT_NEW_PATH] text_old_path
```

## Tools

### Find Strings

Searches 2-columns `.tsv` files in a given directory for two corresponding strings `old` and `new`.
Prints files, rows and lines where both strings appear.

```bash
python -m aba.find_strings [-h] [-d DIRECTORY] old new
```

## Run Tests

```bash
py.test
```