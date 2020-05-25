import requests
from os import remove
from datetime import datetime

# Ниже необходимо указать ссылку на свой плейлист из ЛК iedem
url = 'http://iedem.tv/playlists/uplist/your_id/playlist.m3u8'
myfile = requests.get(url)
open('temp.m3u8', 'wb').write(myfile.content)
json_list = []
temp_lst = []
favorites_lst = []
temp_lst1 = []
temp = 0
with open('temp.m3u8', 'r', encoding='utf-8') as f:
    temp_dict = {}
    for i in f:
        if '#EXTINF' in i:
            temp_dict['tvg-name'] = i.split(',')[1].strip()
            temp_dict['tvg-rec'] = i.split(',')[0][10:]
            temp_dict['tvg-logo'] = 'https://tv.sdckz.com/logo/' + temp_dict['tvg-name'].replace(' ', '') + '.png'
        elif '#EXTGRP' in i:
            temp_dict['group-title'] = i.replace('#EXTGRP:', '').strip()
        elif 'http' in i:
            temp_dict['link'] = i.strip()
            json_list.append(temp_dict)
            temp_dict = {}
remove('temp.m3u8')
with open('temp.m3u8', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U x-tvg-url="http://epg.it999.ru/epg.xml.gz"\n')
    for d in json_list:
        # Ниже во второй квадратной скобке указываем группы через запятую, которые необходимо исключить
        if d['group-title'] not in ['Հայկական', 'українські', 'беларускія', 'azərbaycan', 'ქართული', 'точик', 'moldovenească', 'türk', 'o\'zbek', 'ישראלי']:
            f.write(f'''#EXTINF:0 group-title="{d['group-title']}" tvg-name="{d['tvg-name']}" tvg-logo="{d['tvg-logo']}" {d['tvg-rec']},{d['tvg-name']}''' + '\n')
            f.write(d['link'] + '\n')
with open('temp.m3u8', 'r', encoding='utf-8') as f:
    for k in f:
        temp_lst.append(k)
with open('favorites.txt', 'r', encoding='utf-8') as f:
    for k in f:
        k = k.strip()
        favorites_lst.append(k)
while temp < len(favorites_lst):
    with open('temp.m3u8', 'r', encoding='utf-8') as f:
        for k in f:
            if favorites_lst[temp] in k:
                temp_lst1.append(k)
                temp_lst.remove(k)
                j = next(f)
                temp_lst.remove(j)
                temp_lst1.append(j)
        temp += 1
dtime = datetime.now().strftime('%Y%m%d%H%M%S')
with open(f'iedemtv_{dtime}.m3u8', 'w', encoding='utf-8') as f:
    temp_lst.remove('#EXTM3U x-tvg-url="http://epg.it999.ru/epg.xml.gz"\n')
    f.write('#EXTM3U x-tvg-url="http://epg.it999.ru/epg.xml.gz"\n')
    for k in temp_lst1:
        f.write(k)
    for k in temp_lst:
        f.write(k)
remove('temp.m3u8')
