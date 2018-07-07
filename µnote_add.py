#! /usr/bin/python3

import argparse
import json
import subprocess


try:
    with open('data/notes.json') as f:
        notes = json.load(f)
except FileNotFoundError:
    notes = []

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--media-comment')
parser.add_argument('-l', '--media-link')
parser.add_argument('-f', '--media-file')
group = parser.add_mutually_exclusive_group()
group.add_argument('-s', '--reply-self')
group.add_argument('-u', '--reply-url')
parser.add_argument('-U', '--reply-title')
group.add_argument('-r', '--reply-to')
parser.add_argument('-t', '--reply-quote')
parser.add_argument('-i', '--reply-time')
parser.add_argument('text')
args = parser.parse_args()
if any([args.media_comment, args.media_link, args.media_file]) and not \
   all([args.media_comment, args.media_link, args.media_file]):
    raise argparse.ArgumentTypeError('Media posts require -c, -l and -f')
if any([args.reply_url, args.reply_title]) and not \
   all([args.reply_url, args.reply_title]):
    raise argparse.ArgumentTypeError('URL replies require -u and -U')
elif any([args.reply_to, args.reply_quote, args.reply_time]) and not \
   all([args.reply_to, args.reply_quote, args.reply_time]):
    raise argparse.ArgumentTypeError('Toot replies require -r, -t and -i')

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
notes.append(note)

with open('data/notes.json', 'w') as f:
    json.dump(notes, f, indent=4, sort_keys=True)
