# Installation guide

- Install Python >=3.7

- Install youtube-dl via pip using command ```pip install youtube-dl```
- Install eyed3 via pip using command ```pip install eyed3```
- Install requests via pip using command ```pip install requests```


- Install Chocolate
    - Run Powershell as Administrator
    - Execute ```Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))```
- Install ffmpeg via chocolate
    - execute command ```choco install ffmpeg```

- execute command ```git clone https://github.com/BIG293/youtube2mp3.git``` in order to clone the repository

# Execution

- Run the ytdownload.py from terminal and enter the url to download
- The script automatically downloads the file or the playlist entered and tries to rename the file and sets metadata of the mp3. If something goes wrong it moves the mp3 to the "NEED_ACTION!!!" folder. In this way, if you want, you can execute some manual actions to edit your downloaded mp3.
- For debbugging purpose it saves for each songs, on "entriesjson" folder, a json with the corresponding information downloaded from YouTube
