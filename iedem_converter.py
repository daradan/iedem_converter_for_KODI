from requests import get


# Ниже необходимо указать ссылку на свой плейлист из ЛК iedem
url = 'http://iedem.tv/playlists/uplist/your_id/playlist.m3u8'
playlist = get(url)

json_list = []
playlist_list = []
temp_dict = {}
group_edited_list = []
favorites_list = []
num_on_list = []
temp_num = 0

playlist.encoding = 'utf-8'
for playlist_line in playlist.text.split('\n'):
    playlist_list.append(playlist_line.strip('\r'))

for playlist_line_2 in playlist_list:
    if '#EXTINF' in playlist_line_2:
        temp_dict['tvg-name'] = playlist_line_2.split(',')[1].strip()
        temp_dict['tvg-rec'] = playlist_line_2.split(',')[0][10:]
        temp_dict['tvg-logo'] = 'https://tv.sdckz.com/logo/' + temp_dict['tvg-name'].replace(' ', '') + '.png'
    elif '#EXTGRP' in playlist_line_2:
        temp_dict['group-title'] = playlist_line_2.replace('#EXTGRP:', '').strip()
    elif 'http' in playlist_line_2:
        temp_dict['link'] = playlist_line_2.strip()
        json_list.append(temp_dict)
        temp_dict = {}

for playlist_line_3 in json_list:
    # Ниже во второй квадратной скобке указываем группы через запятую, которые необходимо исключить
    if playlist_line_3['group-title'] not in ['Новый сайт - edemtv.me', 'Հայկական', 'українські', 'беларускія',\
                                              'azərbaycan', 'ქართული', 'точик', 'moldovenească', 'türk', 'o\'zbek',\
                                              'ישראלי']:
        group_edited_list.append(f'''#EXTINF:0 group-title="{playlist_line_3['group-title']}"\
 tvg-name="{playlist_line_3['tvg-name']}" tvg-logo="{playlist_line_3['tvg-logo']}"\
 {playlist_line_3['tvg-rec']},{playlist_line_3['tvg-name']}''')
        group_edited_list.append(playlist_line_3['link'])

with open('favorites.txt', 'r', encoding='utf-8') as fav_file:
    for fav_channel in fav_file:
        favorites_list.append(fav_channel.strip())

while temp_num < len(favorites_list):
    for num, val in enumerate(group_edited_list):
        if favorites_list[temp_num] in val:
            if favorites_list[temp_num] == val.split('"')[3]:
                num_on_list.append(num)
                num_on_list.append(num + 1)
    temp_num += 1

pre_finish_fav_list = ['#EXTM3U x-tvg-url="http://epg.it999.ru/epg.xml.gz"']
for k in num_on_list:
    pre_finish_fav_list.append(group_edited_list[k])

for i in sorted(num_on_list, reverse=True):
    del group_edited_list[i]
del group_edited_list[0]
finish_fav_list_both = pre_finish_fav_list + group_edited_list

with open('pl.m3u8', 'w', encoding='utf-8') as fin_file:
    for j in finish_fav_list_both:
        fin_file.write(j + '\n')
