## rules

* add rules → see what is left → add new rules → etc.
* use needlemann-wunsch to align characters in words
* how to use google spreadsheet for analysis ?

## align words

* code presentation : order of functions (main before or after defs ?)
* add column names to .tsv ?
* use urls to download single raw files from github instead of downloading whole repo

### alignment

ambiguous alignment on compound words

```
['&', 'MARIE', 'TERESE', 'perit', 'pour', 'toute', 'la', 'terre', '.']
['¤', 'et', 'MARIE-THÉRÈSE', 'périt', 'pour', 'toute', 'la', 'terre', '.']
```

gives

```
['& MARIE', 'TERESE', 'perit', 'pour', 'toute', 'la', 'terre', '.']
['et', 'MARIE-THÉRÈSE', 'périt', 'pour', 'toute', 'la', 'terre', '.']
```

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

#### list of cases

* `IV` + `¤` → `IV` and `IV` + `.` → `IV.`