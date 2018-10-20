#! /usr/bin/python3

import json
import re
import textwrap

from jnrbase.attrdict import AttrDict


with open('data/notes.json') as f:
    notes = json.load(f, object_hook=AttrDict)


for note in notes:
    note.text = re.sub(r'@([@\w]+)@(\w+)',
                       r'@<\1 https://mastodon.\2/\1/twtxt.txt>',
                       note.text)
    first = True
    for chunk in textwrap.wrap(note.text, 140):
        print(f'{note.timestamp}	{"" if first else "…"}{chunk}')
        first = False
