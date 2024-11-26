# ABA

Alignment-Based Approach for automatic modernization of french texts from the 17th to the 18th century

Online demo at https://igm.univ-mlv.fr/~gambette/text-processing/aba/

## Install

### Install Packages

* With make

```bash
make
```

* Without make

Add an extra line with ASR_metrics in the end of the file requirements.txt if you want to use the evaluation metrics

```bash
pip install -r requirements.txt
```

### Generate Data

#### Download, Align and Analyze FreEMnorm

1. Download [FreEMnorm](https://github.com/FreEM-corpora/FreEMnorm) and put it into the `download` folder or run script

```bash
python -m aba.download_git 'https://github.com/FreEM-corpora/FreEMnorm.git'
```

2. Align FreEMnorm by words

```bash
python -m aba.align_words
```

3. Extract dictionaries from FreEMnorm

```bash
python -m aba.analyze
```

#### Extract Morphalou Dictionary

1. Download [Morphalou](https://www.ortolang.fr/market/lexicons/morphalou)
2. Copy `morphalou/5/Morphalou3.1_formatCSV_toutEnUn/Morphalou3.1_CSV.csv` to `download` folder
3. Run script

```bash
python -m aba.extract_dic_morphalou
```

#### Extract Wikisource Dictionary

Extract *old french → modern french* dictionary from [Wikisource](https://fr.wikisource.org/wiki/Wikisource:Dictionnaire).

```bash
python -m aba.extract_dic_wikisource
```

#### Extract Name Dictionary

Extract dictionary from multiple `.dic` files located in `resources` folder.

```bash
python -m aba.extract_dic_resources
```

## Main Scripts

### Modernize Corpus

```bash
python -m aba.modernize_corpus
```

### Modernize Text

Modernize a text in Middle French. [^*]

```bash
python -m aba.modernize [-h] middle_french_text_path
```

### Modernize Text and Evaluate It

Modernize a text in Middle French and evaluate it by comparing it with a reference version stored in a file TEXT_NEW_PATH

```bash
python -m aba.modernize_and_evaluate [-h] -n NORMALISED_TEXT_PATH middle_french_text_path
```

## Tools

### Rules Chart

Opens a labeled dictionary and displays an interactive `plotly` pie chart showing the frequence of modernization rules. A copy of the chart is saved in `data/rules_chart.html`.

```bash
python -m aba.rules_chart
```

### Find Strings

Search 2-columns `.tsv` files in a given directory for two corresponding strings `old` and `new`.
Prints files, rows and lines where both strings appear.

```bash
python -m aba.find_strings [-h] [-d DIRECTORY] old new
```

### Produce plots of the evolution per rule

Search 2-columns `.tsv` files in a given directory, search for spelling variation between `.src` and `.trg`, produce a plot with the evolution of each rule. It requires to run `python -m aba.rules_chart` first.

```bash
python -m aba.rules_sum.py
```

### Run Tests

```bash
py.test
```

[^*]: Path arborescence must be written with forward slashes `/`.
