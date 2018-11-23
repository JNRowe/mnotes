#! /usr/bin/python3

import json
import sys

from jnrbase.attrdict import AttrDict
from lxml import html


with open(sys.argv[1]) as f:
    page = html.parse(f)

with open('data/notes.json') as f:
    notes = json.load(f, object_hook=AttrDict)

with open('data/config.json') as f:
    config = json.load(f, object_hook=AttrDict)

feed = AttrDict(
    version='https://jsonfeed.org/version/1',
    title='James Rowe',
    icon='https://micro.blog/JNRowe/avatar.jpg',
    home_page_url='https://jnrowe.github.com/mnotes/',
    feed_url='https://jnrowe.github.com/mnotes/feed.json',
    description=config.subtitle,
    author={
        'name': config.author.name,
        'url': config.author.uri,
    },
    items=[]
)

for note, post in list(zip(reversed(notes),
                           page.getroot().cssselect('.note')))[:15]:
    loc = f'{config.url}#TS{note.timestamp}'
    content = html.tostring(post, True).decode()
    content = content.strip().replace('\n', '')
    item = AttrDict(
        id=loc,
        content_html=content,
        content_text=note.text,
        date_published=note.timestamp,
        url=loc,
    )
    if 'media' in note:
        item.image = f'{config.url}media/{note.media.file}'
    feed['items'].append(item)


print(json.dumps(feed, indent=4))
