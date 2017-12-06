#! /usr/bin/python3

import json
import re

import jinja2


ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'))
HTML_FILTERS = {
    re.compile(r'(#\w+)'): r'<b>\1</b>',
    re.compile(r'(https?://[\w\.?=\+/_-]+)', re.IGNORECASE):
        r'<a href="\1">\1</a>',
}


def htmlise(dct):
    if 'text' in dct:
        for pat, repl in HTML_FILTERS.items():
            dct['text'] = re.sub(pat, repl, dct['text'])
    return dct


with open('data/notes.json') as f:
    notes = json.load(f, object_hook=htmlise)

tmpl = ENV.get_template('notes.jinja')

print(tmpl.render(notes=notes))
