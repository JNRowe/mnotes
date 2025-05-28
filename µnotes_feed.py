#!/usr/bin/env python3

import itertools
import json
import sys

from ciso8601 import parse_rfc3339
from jnrbase.attrdict import AttrDict
from lxml import html
from feedwerk.atom import AtomFeed


with open(sys.argv[1]) as f:
    page = html.parse(f)

with open("data/µnotes.json") as f:
    notes = json.load(f, object_hook=AttrDict)

with open("data/config.json") as f:
    config = json.load(f, object_hook=AttrDict)

feed = AtomFeed(**config)
for note, post in itertools.islice(
    zip(reversed(notes), page.getroot().cssselect(".note")), 15
):
    title = note.text
    content = html.tostring(post, True).decode()
    content = content.strip().replace("\n", "")
    time = parse_rfc3339(post.cssselect("p.meta time")[0].get("datetime"))
    feed.add(
        title=title,
        content=content,
        content_type="html",
        url="%s#%s" % (config.url, post.get("id")),
        updated=time,
        published=time,
        xml_base=config.url,
    )

print(feed.to_string())
