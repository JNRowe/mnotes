#! /usr/bin/python3

import json
import subprocess
import sys


try:
    with open('data/notes.json') as f:
        notes = json.load(f)
except FileNotFoundError:
    notes = []

ts = subprocess.check_output(['date', '-Iseconds']).decode().strip()
notes.append({
    'text': sys.argv[1],
    'timestamp': ts,
})

with open('data/notes.json', 'w') as f:
    json.dump(notes, f, indent=4, sort_keys=True)
