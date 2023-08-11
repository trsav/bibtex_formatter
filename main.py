import re
from difflib import SequenceMatcher
import numpy as np 
from tqdm import tqdm
import json

def read_json(path):
    # read a json file as a dictionary
    with open(path, "r") as f:
        data = json.load(f)
    return data


def read_bibtex(path):
    with open(path, "r") as f:
        data = [j.replace('\n', '') for j in f.readlines()]
    return data

letters = ["0-9","A", "B", "C", "D", "E", "F", "G", "H", "I",
              "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                "S", "T", "U", "V", "W", "X", "Y", "Z"]


def parse_bibtex(bib):

    entries = []
    i = 0 
    while i < len(bib):
        l = bib[i]
        if len(l) == 0:
            i += 1
            continue
        if "@" in l:
            start = i 
            c = 1
            i += 1
            continue
        else:

            c += l.count("{")
            c -= l.count("}")

            if c == 0:
                end = i+1
                entry = "\n".join(bib[start:end])
                entries.append(entry)
            i += 1
            continue
    return entries


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def replace_journal(bib_entry,a_dicts):
    try:
        journal = re.search("journal *= *(\{+)(.*)\}", bib_entry).group(2)
    except AttributeError:
        print("No journal entry found (not a journal article?)")
        return bib_entry
    first_letter = journal[0].upper()
    if first_letter.isdigit():
        first_letter = "0-9"
    a_dict = a_dicts[first_letter]
    journals = list(a_dict.keys())
    # if the journal name is 'arxiv' or contains 'arxiv'...
    if 'arxiv' in journal.lower():
        print("Journal name is "+journal+". So I will skip...")
        return bib_entry
    sim = []
    for j in journals:
        sim.append(similar(journal.upper(), j))
    max_sim = np.argmax(np.array(sim))
    matching_journal = journals[max_sim]
    matching_abbrev = a_dict[matching_journal]
    print(journal +' --> '+matching_journal +' --> '+ matching_abbrev)
    # replace the journal in {} with the matching_abbrev
    bib_entry = bib_entry.replace(journal, matching_abbrev)

    return bib_entry

def title_format(bib_entry):
    # ensure title is double-braced
    # if {{}} then fine. if {} then add another {}
    try:
        title = re.search("title *= *(\{+)(.*)\}", bib_entry).group(2)
    except AttributeError:
        print("No title entry found... hmmmm.")
        return bib_entry
    if title[0] == '{' and title[-1] == '}':
        return bib_entry
    else:
        bib_entry = bib_entry.replace(title, "{"+title+"}")
        print('Added double curly braces to title!')
        return bib_entry
    return bib_entry

def update_bib(bib_path):
    print('Reading Abbreviations')
    a_dicts = read_json("data/overall.json")

    bib = read_bibtex(bib_path)
    entries = parse_bibtex(bib)

    lines = []
    for entry in tqdm(entries):
        lines.append(title_format(replace_journal(entry,a_dicts)))

    # save lines to new bib file 
    with open(bib_path+"_abbreviated.bib", "w") as f:
        f.write("\n".join(lines))
    return 

def main():
    path = input("Enter path to bibtex file: ")
    update_bib(path)
    return 

if __name__ == "__main__":
    main()