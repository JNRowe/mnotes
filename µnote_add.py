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
parser.add_argument('-r', '--reply-to')
parser.add_argument('-t', '--reply-quote')
parser.add_argument('-i', '--reply-time')
parser.add_argument('text')
args = parser.parse_args()
if any([args.reply_to, args.reply_quote, args.reply_time]) and not \
   all([args.reply_to, args.reply_quote, args.reply_time]):
    raise argparse.ArgumentTypeError('Replies require -r, -t and -i')

ts = subprocess.check_output(['date', '-Iseconds']).decode().strip()
note = {
    'text': args.text,
    'timestamp': ts,
}
if args.reply_to:
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
