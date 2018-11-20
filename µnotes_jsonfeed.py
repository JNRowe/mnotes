#! /usr/bin/python3

import json

from jnrbase.attrdict import AttrDict


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

for note in reversed(notes):
    loc = f'{config.url}#TS{note.timestamp}'
    item = AttrDict(
        id=loc,
        content_text=note.text,
        date_published=note.timestamp,
        url=loc,
    )
    if 'media' in note:
        item.image = f'{config.url}media/{note.media.file}'
    feed['items'].append(item)


print(json.dumps(feed, indent=4))
