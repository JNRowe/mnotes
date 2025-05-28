#!/usr/bin/env python3

import argparse
import json
import os
import subprocess

import ciso8601


def existing_file(s: str) -> str:
    path = f'data/media/{s}'
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f'Missing file {path!r}')
    return s


def valid_timestamp(s: str) -> str:
    try:
        ciso8601.parse_rfc3339(s)
    except ValueError as e:
        raise argparse.ArgumentTypeError(e.args[0])
    return s


try:
    with open('data/µnotes.json') as f:
        notes = json.load(f)
except FileNotFoundError:
    notes = []

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--media-comment', help="comment for media element",
                    metavar='text')
parser.add_argument('-l', '--media-link', help="link for media element",
                    metavar='url')
parser.add_argument('-f', '--media-file', type=existing_file,
                    help="file for media element", metavar='file')
parser.add_argument('-e', '--reference-url', action='append',
                    help='link for reference', metavar='url')
parser.add_argument('-E', '--reference-title', action='append',
                    help='title for reference', metavar='text')
group = parser.add_mutually_exclusive_group()
group.add_argument('-s', '--reply-self', type=valid_timestamp,
                   help='timestamp of referenced note', metavar='timestamp')
group.add_argument('-u', '--reply-url', help='link for referenced URL',
                   metavar='url')
parser.add_argument('-U', '--reply-title', help='title for reply',
                    metavar='text')
group.add_argument('-r', '--reply-to', help='user for reply', metavar='user')
parser.add_argument('-t', '--reply-quote', help='referenced note’s content',
                    metavar='text')
parser.add_argument('-i', '--reply-time', type=valid_timestamp,
                    help='timestamp of referenced note', metavar='timestamp')
parser.add_argument('-m', '--importance',
                    choices=['perhaps', 'should', 'must'],
                    help='importance advice', metavar='importance')
parser.add_argument('-g', '--urgency', choices=['whenever', 'soon', 'now'],
                    help='urgency advice', metavar='urgency')
parser.add_argument('text', help="content of note to post")
args = parser.parse_args()
if any([args.media_comment, args.media_link, args.media_file]) and not \
   all([args.media_comment, args.media_link, args.media_file]):
    raise argparse.ArgumentTypeError('Media posts require -c, -l and -f')
if any([args.reference_url, args.reference_title]) and not \
   all([args.reference_url, args.reference_title]):
    raise argparse.ArgumentTypeError('References require -e and -E')
if args.reference_url and \
   len(args.reference_url) != len(args.reference_title):
    raise argparse.ArgumentTypeError("Inconsistent number of -e and -E")
if any([args.reply_url, args.reply_title]) and not \
   all([args.reply_url, args.reply_title]):
    raise argparse.ArgumentTypeError('URL replies require -u and -U')
elif any([args.reply_to, args.reply_quote, args.reply_time]) and not \
   all([args.reply_to, args.reply_quote, args.reply_time]):
    raise argparse.ArgumentTypeError('Toot replies require -r, -t and -i')
if any([args.importance, args.urgency]) and not \
   all([args.importance, args.urgency]):
    raise argparse.ArgumentTypeError('Advice information requires -m and -g')

ts = subprocess.check_output(['date', '-Iseconds']).decode().strip()
note = {
    'text': args.text,
    'timestamp': ts,
}
if args.media_comment:
    note['media'] = {
        'comment': args.media_comment,
        'link': args.media_link,
        'file': args.media_file,
    }
if args.reference_url:
    note['references'] = [{'title': t, 'url': u}
                          for t, u in zip(args.reference_title,
                                          args.reference_url)]
if args.reply_self:
    note['in_reply_url'] = {
        'self': args.reply_self,
    }
elif args.reply_url:
    note['in_reply_url'] = {
        'title': args.reply_title,
        'url': args.reply_url
    }
elif args.reply_to:
    note['in_reply_to'] = {
        'text': args.reply_quote,
        'toot': {
            'timestamp': args.reply_time,
            'user': args.reply_to,
        }
    }
if args.importance:
    note['x-advice'] = {
        'importance': args.importance,
        'urgency': args.urgency,
    }
notes.append(note)

with open('data/µnotes.json', 'w') as f:
    json.dump(notes, f, indent=4, sort_keys=True)
