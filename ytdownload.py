from __future__ import unicode_literals
import json
import os
import re
import shutil
import requests
import eyed3
from youtube_dl import YoutubeDL as ydl


ENTRY_DIR = 'entriesjson'
DOWNLOADS_DIR = 'downloads'
TO_DOWNLOAD_PATH = './to-download.txt'
NEEDS_ACTION = 'downloads/NEEDS_ACTION!!!'

YLD_OPTIONS = {
    'format':
    'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s'
}


def extract_url(entry):
    return entry['webpage_url']


def has_artist(entry):
    return 'artist' in entry and entry['artist'] is not None


def title_already_contains_artist(entry):
    return entry['artist'] in entry['title']


def compute_out_tmpl(info, options):
    if has_artist(info) and not title_already_contains_artist(info):
        options['outtmpl'] = 'downloads/%(artist)s - %(title)s.%(ext)s'
    else:
        options['outtmpl'] = 'downloads/%(title)s.%(ext)s'
    return options


def download_songs():
    try:
        os.stat(TO_DOWNLOAD_PATH)
    except Exception as err:
        print(err)
        open(TO_DOWNLOAD_PATH, "w+")

    file_list = open(TO_DOWNLOAD_PATH, 'r')

    for url in file_list:
        url_info = ydl().extract_info(url, download=False)

        entries = []

        if 'entries' in url_info:
            entries = url_info['entries']
        else:
            entries = [url_info]

        for entry in entries:
            title = entry['title']

            try:
                os.stat(ENTRY_DIR)
            except Exception as err:
                print(err)
                os.mkdir(ENTRY_DIR)

            title = re.sub('[<>:"/\|?*]', '', title)
            with open("% s/% s.json" % (ENTRY_DIR, title), 'w') as outfile:
                json.dump(entry, outfile)

            try:
                os.stat(DOWNLOADS_DIR)
            except Exception as err:
                print(err)
                os.mkdir(DOWNLOADS_DIR)

            ydl(YLD_OPTIONS).download([extract_url(entry)])
            set_metadata(entry)


def set_metadata(entry):
    audiofile = eyed3.load(
        f'./{DOWNLOADS_DIR}/{entry["title"]}.mp3')
    if len(entry['thumbnails']) > 0:
        max_index = max(range(
            len(entry['thumbnails'])), key=lambda index: entry['thumbnails'][index]['width'])
        response = requests.get(entry['thumbnails'][max_index]['url'])
        if response.ok:
            audiofile.tag.images.set(
                3, response.content, 'image/png')

    if 'artist' in entry:
        audiofile.tag.artist = entry['artist']
    if 'title' in entry:
        audiofile.tag.title = entry['title']
    audiofile.tag.save()

    if(not has_artist(entry) or title_already_contains_artist(entry)):
        try:
            os.stat(NEEDS_ACTION)
        except Exception as err:
            print(err)
            os.mkdir(NEEDS_ACTION)
        title = entry['title']
        shutil.move(f'{DOWNLOADS_DIR}/{title}.mp3',
                    f'{NEEDS_ACTION}')


def improve_file_names(directory):
    for _count, filename in enumerate(os.listdir(directory)):
        try:
            dst=re.sub('[\[|(].*?[\]|)]', '', filename)
            splitted=dst.split('.')
            ext=splitted.pop(len(splitted) - 1)
            name=''.join(splitted).strip()
            name_ext=name + '.' + ext
            os.rename('% s/% s' % (directory, filename),
                      '% s/% s' % (directory, name_ext))
        except Exception as err:
            print(err)
            print('AN ERROR HAS OCCURED RENAMING: % s' % (filename))


download_songs()
improve_file_names(DOWNLOADS_DIR)
