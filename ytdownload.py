from __future__ import unicode_literals
import youtube_dl

YLD_OPTIONS = {
    'outtmpl': 'downloads/%(title)s-%(id)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def download_songs():
    file_list = open('./to-download.txt', 'r')

    with youtube_dl.YoutubeDL(YLD_OPTIONS) as ydl:
        url_list = []
        for url in file_list:
            url_list.append(url)
        ydl.download(url_list)


download_songs()
