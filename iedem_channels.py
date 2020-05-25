import requests
from os import remove


url = 'http://c0216f381ef0.yourlistbest.net/playlists/uplist/e379294660ff4ff6ea21eefd6a2ae8df/playlist.m3u8'
myfile = requests.get(url)
open('temp.m3u8', 'wb').write(myfile.content)
json_list = []
with open('temp.m3u8', 'r', encoding='utf-8') as f:
    for k in f:
        if '#EXTINF' in k:
            json_list.append(k.split(',')[1].strip())
json_list.sort()
with open('iedem_channels_sorted.txt', 'w', encoding='utf-8') as f:
    for k in json_list:
        f.write(k + '\n')
remove('temp.m3u8')
