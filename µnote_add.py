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
parser.add_argument('-c', '--media-comment', help="comment for media element",
                    metavar='text')
parser.add_argument('-l', '--media-link', help="link for media element",
                    metavar='url')
parser.add_argument('-f', '--media-file', help="file for media element",
                    metavar='file')
parser.add_argument('-e', '--reference-url', action='append',
                    help='link for reference', metavar='url')
parser.add_argument('-E', '--reference-title', action='append',
                    help='title for reference', metavar='text')
group = parser.add_mutually_exclusive_group()
group.add_argument('-s', '--reply-self', help='timestamp of referenced note',
                   metavar='timestamp')
group.add_argument('-u', '--reply-url', help='link for referenced URL',
                   metavar='url')
parser.add_argument('-U', '--reply-title', help='title for reply',
                    metavar='text')
group.add_argument('-r', '--reply-to', help='user for reply', metavar='user')
parser.add_argument('-t', '--reply-quote', help='referenced note’s content',
                    metavar='text')
parser.add_argument('-i', '--reply-time', help='timestamp of referenced note',
                    metavar='timestamp')
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
notes.append(note)

with open('data/notes.json', 'w') as f:
    json.dump(notes, f, indent=4, sort_keys=True)
