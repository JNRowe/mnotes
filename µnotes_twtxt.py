#! /usr/bin/python3

import json
import re
import textwrap

from jnrbase.attrdict import AttrDict


with open('data/µnotes.json') as f:
    notes = json.load(f, object_hook=AttrDict)


for note in notes:
    note.text = re.sub(r'@([@\w]+)@(\w+)',
                       '@<\\1\N{US}https://mastodon.\\2/\\1/twtxt.txt>',
                       note.text)
    if note.text.startswith(('.@', '@')):
        at = note.text[:note.text.find('>') + 1].replace('\N{US}', ' ')
        text = note.text[note.text.find('>') + 1:]
    else:
        at = ''
        text = note.text
    first = True
    for chunk in textwrap.wrap(text, 139 - len(at)):
        print(note.timestamp, '\t', at, '' if first else '… ',
              chunk.replace('\N{US}', ' '), sep='')
        first = False
