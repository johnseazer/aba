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

## Run

```
python -m fren
```

* Downloads [PARALLEL17](https://github.com/e-ditiones/PARALLEL17) corpus
* Aligns PARALLEL17 by words
* Creates corresponding dictionary with occurence count
* Completes dictionary with additional data

## Run Tests

```bash
py.test
```