# ABA

Alignment-Based Approach for automatic modernization of french texts from the 16th to the 18th century

## Install

### Install Packages

* With make

```bash
make
```

* Without make

```bash
pip install -r requirements.txt
```

### Generate Data

#### Download, Align and Analyze PARALLEL17

1. Download [PARALLEL17](https://github.com/e-ditiones/PARALLEL17) and put it into the `download` folder or run script

```bash
python -m aba.download_git 'https://github.com/PhilippeGambette/PARALLEL17.git'
```

2. Align PARALLEL17 by words

```bash
python -m aba.align_words
```

3. Extract dictionaries from PARALLEL17

```bash
python -m aba.analyze
```

#### Extract Morphalou Dictionary

1. Download [Morphalou](https://www.ortolang.fr/market/lexicons/morphalou)
2. Copy `morphalou/4/Morphalou3.1_formatCSV_toutEnUn/Morphalou3.1_CSV.csv` to `download` folder
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

Modernize a text in old french. [^*]

```bash
python -m aba.modernize [-h] [-n TEXT_NEW_PATH] text_old_path
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

### Run Tests

```bash
py.test
```

[^*]: Path arborescence must be written with forward slashes `/`.