#! /usr/bin/python3

import json
import re
import textwrap

from jnrbase.attrdict import AttrDict


with open('data/notes.json') as f:
    notes = json.load(f, object_hook=AttrDict)


for note in notes:
    note.text = re.sub(r'@([@\w]+)@(\w+)',
                       '@<\\1\N{US}https://mastodon.\\2/\\1/twtxt.txt>',
                       note.text)
    if note.text.startswith(('.@', '@')):
        at = note.text[:note.text.find('>') + 1].replace('\N{US}', ' ')
    else:
        at = ''
    first = True
    for chunk in textwrap.wrap(note.text, 140 - len(at)):
        print(f'{note.timestamp}\t', end='')
        if not first:
            if at:
                print(f'{at}… ', end='')
            else:
                print('… ', end='')
        print(chunk.replace('\N{US}', ' '))
        first = False
