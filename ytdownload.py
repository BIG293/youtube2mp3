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
TO_DOWNLOAD_PATH = './to-download.txt'


def extract_url(entry):
    return entry['webpage_url']


def has_artist(entry):
    return 'artist' in entry and entry['artist'] is not None


def title_already_contains_artist(entry):
    return entry['artist'] in entry['title']


def compute_out_tmpl(info, options):
    try:
        os.stat(DOWNLOADS_DIR)
    except Exception as e:
        print(e)
        os.mkdir(DOWNLOADS_DIR)
        
    if has_artist(info) and not title_already_contains_artist(info):
        options['outtmpl'] = 'downloads/%(artist)s - %(title)s.%(ext)s'
    else:
        options['outtmpl'] = 'downloads/%(title)s.%(ext)s'
    return options


def download_songs():
    try:
        os.stat(TO_DOWNLOAD_PATH)
    except Exception as e:
        print(e)
        open(TO_DOWNLOAD_PATH,"w+")

    file_list = open(TO_DOWNLOAD_PATH, 'r')

    for url in file_list:
        url_info = ydl().extract_info(url, download=False)

        entries = []

        if 'entries' in url_info:
            entries = url_info['entries']
        else:
            entries = [url_info]

        for entry in entries:
            t = entry['title']

            try:
                os.stat(ENTRY_DIR)
            except Exception as e:
                print(e)
                os.mkdir(ENTRY_DIR)

            title = re.sub('[<>:"/\|?*]', '', t)
            with open("% s/% s.json" % (ENTRY_DIR, title), 'w') as outfile:
                json.dump(entry, outfile)

            ydl(compute_out_tmpl(entry, YLD_OPTIONS)).download(
                [extract_url(entry)])


def improve_file_names():
    for _count, filename in enumerate(os.listdir(DOWNLOADS_DIR)):
        try:
            dst = re.sub('[\[|(].*?[\]|)]', '', filename)
            splitted = dst.split('.')
            ext = splitted.pop(len(splitted) - 1)
            name = ''.join(splitted).strip()
            name_ext = name + '.' +ext
            os.rename('% s/% s' % (DOWNLOADS_DIR, filename),
                      '% s/% s' % (DOWNLOADS_DIR, name_ext))
        except Exception as e:
            print(e)
            print('AN ERROR HAS OCCURED RENAMING: % s' % (filename))


download_songs()
improve_file_names()
