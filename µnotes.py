#! /usr/bin/env python3

import datetime
import html
import json
import re

from pathlib import Path
from typing import Dict, Optional
from xml.sax.saxutils import quoteattr

import jinja2

from ciso8601 import parse_rfc3339
from jnrbase.attrdict import AttrDict


def tag(
    name: str,
    attribs: Optional[Dict[str, str]] = None,
    text: Optional[str] = r"\1",
) -> str:
    if attribs:
        attrib_string = " " + " ".join(
            "%s=%s" % (k, quoteattr(v)) for k, v in attribs.items()
        )
    else:
        attrib_string = ""
    res = "\N{STX}%s%s\N{ETX}" % (name, attrib_string)
    if text:
        res += "%s\N{STX}/%s\N{ETX}" % (text, name)
    return res


def _abbrrevise(s: str) -> str:
    return "".join(s[0] for s in s.replace("-", " ").split())


with Path("data/abbrevs.dat").open() as f:
    ABBREV_STRINGS = [l.strip() for l in f]
ABBREVS = {
    re.compile(r"\b%s\b" % _abbrrevise(s)): tag(
        "abbr", {"title": html.escape(s, True)}, _abbrrevise(s)
    )
    for s in ABBREV_STRINGS
}
ENV = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
HTML_FILTERS = {
    re.compile(r"(?<!&)(#[a-zA-Z_]\w+(?=[^\d\S]|\W))", re.IGNORECASE): tag("b"),
    re.compile(r"(https?://[\w\.?=\+/_-]+)", re.IGNORECASE): tag(
        "a", {"href": r"\1"}
    ),
    re.compile(r"\B(@\w+(?:@\w+)*)"): tag("em"),
    re.compile(r"\B/(\w+)/\B"): tag("em"),
    re.compile(r"\*((?:(?:[\w’]+)\W?)+)\*"): tag("strong"),
    re.compile(r"``(.*?)``"): tag("code"),
    re.compile(r"\n"): tag("br", text=None),
}


def munge(dct: Dict[str, str]) -> AttrDict:
    dct = AttrDict(**dct)
    if "text" in dct:
        dct.text = html.escape(dct.text)
        for pat, repl in HTML_FILTERS.items():
            dct.text = pat.sub(repl, dct.text)
        for pat, repl in ABBREVS.items():
            dct.text = pat.sub(repl, dct.text)
        dct.text = dct.text.replace("\N{STX}", "<").replace("\N{ETX}", ">")
    if "timestamp" in dct:
        dct.timestamp = parse_rfc3339(dct.timestamp)
    if "self" in dct:
        dct.self = parse_rfc3339(dct.self)
    return dct


with open("data/µnotes.json") as f:
    notes = json.load(f, object_hook=munge)

with open("data/config.json") as f:
    config = json.load(f, object_hook=AttrDict)

tmpl = ENV.get_template("µnotes.jinja")

print(tmpl.render(notes=notes, today=datetime.date.today(), **config))
