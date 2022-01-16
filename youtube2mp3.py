import json
import os
import re
import shutil
import requests
import eyed3
from youtube_dl import YoutubeDL as ydl


ENTRY_DIR = 'entriesjson'
DOWNLOADS_DIR = 'downloads'
NEEDS_ACTION = 'downloads/NEEDS_ACTION!!!'

YLD_OPTIONS = {
    'format':
    'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'cachedire': False,
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
    url = input('Enter the YouTube url to download as mp3 (songs or playlist): ')

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
            os.mkdir(ENTRY_DIR)

        title = re.sub('[<>:"/\|?*]', '', title)
        with open("% s/% s.json" % (ENTRY_DIR, title), 'w') as outfile:
            json.dump(entry, outfile)

        try:
            os.stat(DOWNLOADS_DIR)
        except Exception as err:
            os.mkdir(DOWNLOADS_DIR)

        try:
            ydl(YLD_OPTIONS).download([extract_url(entry)])
        except Exception as e:
            print(e)
            continue

        set_metadata(entry, title)


def set_metadata(entry, title):
    audiofile = eyed3.load(f'./{DOWNLOADS_DIR}/{title}.mp3')
    
    thumbnails_len = len(entry['thumbnails'])
    if thumbnails_len > 0:
        def get_width(index): return entry['thumbnails'][index]['width']
        max_index = max(range(thumbnails_len), key=get_width)
        response = requests.get(entry['thumbnails'][max_index]['url'])
        if response.ok:
            audiofile.tag.images.set(3, response.content, 'image/png')

    if 'artist' in entry:
        audiofile.tag.artist = entry['artist']
    if 'title' in entry:
        audiofile.tag.title = entry['title']
    audiofile.tag.save()

    if(not has_artist(entry) or title_already_contains_artist(entry)):
        try:
            os.stat(NEEDS_ACTION)
        except Exception as err:
            os.mkdir(NEEDS_ACTION)

        shutil.move(f'{DOWNLOADS_DIR}/{title}.mp3',
                    f'{NEEDS_ACTION}')


def improve_file_names(directory):
    for filename in os.listdir(directory):
        try:
            dst = re.sub('[\[|(].*?[\]|)]', '', filename)
            splitted = dst.split('.')
            ext = splitted.pop(len(splitted) - 1)
            name = ''.join(splitted).strip()
            name_ext = name + '.' + ext
            os.rename(f'{directory}/{filename}', f'{directory}/{name_ext}')
        except Exception as err:
            print(err)
            print('AN ERROR HAS OCCURED RENAMING: % s' % (filename))
            continue


if __name__ == '__main__':
    download_songs()
    improve_file_names(DOWNLOADS_DIR)
