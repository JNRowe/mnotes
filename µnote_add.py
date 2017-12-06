#! /usr/bin/python3

import json


notes = []

with open('data/notes.json', 'w') as f:
    json.dump(notes, f, indent=4, sort_keys=True)
