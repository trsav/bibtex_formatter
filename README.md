# Bibtex Formatter

Format titles properly (ensure double curly-brackets) and automatically replace journal titles with their ISO4 abbreviations.

## Instructions

- Clone repository.
```
$ git clone https://github.com/trsav/bibtex_formatter/
```
- Place bibtex file in data folder.
- Run ```main.py``` and specify the bibtex file.
```
$ Enter path to bibtex file: example_bibtex.bib
```
- Wait a bit and enjoy a properly formatted bibtex file.

### Notes
- There are so few dependencies I haven't bothered to include an ```environment.yml``` file, or worse a ```Dockerfile```. Just pip install something if you're missing it. 
- Do proof-read the results, there are probably edge cases. I take no responsibility for anything.
