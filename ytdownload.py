from __future__ import unicode_literals
import json
import os
import re
import string
from youtube_dl import YoutubeDL as ydl

YLD_OPTIONS = {
    'format':
    'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ENTRY_DIR = 'entriesjson'
DOWNLOADS_DIR = 'downloads'


def extract_url(entry):
    return entry['webpage_url']


def has_artist(entry):
    return entry.has_key('artist') and entry['artist'] is not None


def title_already_contains_artist(entry):
    return entry['artist'] in entry['title']


def compute_out_tmpl(info, options):
    if has_artist(info) and not title_already_contains_artist(info):
        options['outtmpl'] = 'downloads/%(artist)s - %(title)s.%(ext)s'
    else:
        options['outtmpl'] = 'downloads/%(title)s.%(ext)s'
    return options


def download_songs():
    file_list = open('./to-download.txt', 'r')

    for url in file_list:
        try:
            url_info = ydl().extract_info(url, download=False)

            entries = []

            if url_info.has_key('entries'):
                entries = url_info['entries']
            else:
                entries = [url_info]

            for entry in entries:
                title = entry['title']

                try:
                    os.stat(ENTRY_DIR)
                except:
                    os.mkdir(ENTRY_DIR)

                with open("% s/% s.json" % (ENTRY_DIR, title), 'w') as outfile:
                    json.dump(entry, outfile)

                ydl(compute_out_tmpl(entry, YLD_OPTIONS)).download(
                    [extract_url(entry)])
        except:
            print 'AN ERROR HAS OCCURED DOWNLOADING: % s' % (url)


def improve_file_names():
    for _count, filename in enumerate(os.listdir(DOWNLOADS_DIR)):
        try:
            dst = re.sub('[\[|(].*?[\]|)]', '', filename)
            splitted = dst.split('.')
            ext = splitted.pop(len(splitted) - 1)
            name = string.join(splitted).strip()
            name_ext = name + '.' +ext
            os.rename('% s/% s' % (DOWNLOADS_DIR, filename),
                      '% s/% s' % (DOWNLOADS_DIR, name_ext))
        except:
            print 'AN ERROR HAS OCCURED RENAMING: % s' % (filename)


download_songs()
improve_file_names()
