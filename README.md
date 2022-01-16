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

- execute command ```git clone https://simonepassaretti@bitbucket.org/simonepassaretti/youtube-mp3.git``` in order to clone the repository
