# Align Words

* Add column names to .tsv ?
* Add `delta_only` as command line option ?
* Use URLs to download single raw files from github instead of downloading whole repo ?

## Alignment

List of bad alignment that needs to be addressed.

* Hyphenation changes

  * Warning : some are correct and must stay unchanged

    ```
    Aulugelle,	Aulu-gelle
    ```

* Bossuet

```
-	TRES
-	HAUTE,
-	TRES
TRESHAUTE,	EXCELLENTE,
TRES-EXCELLENTE,	TRES
TRES-PUISSANTE,	PUISSANTE,
TRES-	TRES
MARIE	-
TERESE	MARIE-THÉRÈSE
AUSTRICHE,	AUTRICHE,
```

```
auſſi-	-
bien	aussi-bien
```

```
-	tout
-	à
tout-à-coup	coup
```

```
par	-
tout	partout
```

```
tarde-t-	-
elle	tarde-t-elle
```

```
Jeſus-	-
Chriſt,	Jésus-Christ,
```

```
MARIE	-
TERESE	MARIE-THÉRÈSE
```

```
-	piété
pieté	aussi
auſſi-bien	bien
```

* Bruyère

```
au	-
delà	au-delà
```

```
quatre-vingt	-
quinze	quatre-vingt-quinze
```

```-	de
de-là	là
```

```
'	’
```

???



# Dico

Extract .tsv dictionary from [wikisource](https://fr.wikisource.org/wiki/Wikisource:Dictionnaire).