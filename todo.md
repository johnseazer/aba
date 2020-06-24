# Notes

* restructure
* algorithms
* tests
* substitution matrix / transition matrix
* data structure for rules
* smith-waterman

## align words

* use urls to download single raw files from github instead of downloading whole repo

### processing empty words

`'¤'` must be concatenated with the word most of the time, but sometimes with previous one

```
['Avec', 'quelle', 'application', '&', 'quelle', 'tendreſſe', 'Philippe', 'IV', '.', 'ſon', 'pere', 'ne', "l'", 'avoit-il', 'pas', 'élevée', '?']
['Avec', 'quelle', 'application', 'et', 'quelle', 'tendresse', 'Philippe', 'IV', '¤', 'son', 'père', 'ne', 'l’', 'avait-il', 'pas', 'élevée', '?']
```

here we need `IV` + `¤` → `IV` so we can have `IV` + `.` → `IV.`, but the current result is

```
['Avec', 'quelle', 'application', '&', 'quelle', 'tendreſſe', 'Philippe', 'IV', '. ſon', 'pere', 'ne', "l'", 'avoit-il', 'pas', 'élevée', '?']
['Avec', 'quelle', 'application', 'et', 'quelle', 'tendresse', 'Philippe', 'IV', 'son', 'père', 'ne', 'l’', 'avait-il', 'pas', 'élevée', '?']
```

(the issue of the space character must be addressed too)

## todo

* compléter repérage auto des types de changements
* approche statistique : voir ce qui change et les premières lettres identiques avant ou après
  * pour toutes les configurations :
    * compter cb de fois les lettres anciennes changent
    * compter cb de fois les lettres anciennes restent identiques
* stocker distances levenshtein pour accélérer traitement ?
* utiliser arguments en ligne de commande/variables globales ?
* découper le module nlptools en plusieurs modules dans un package
* lister les erreurs du corpus parallel17