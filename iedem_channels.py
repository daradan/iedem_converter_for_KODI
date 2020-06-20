from requests import get


# Ниже необходимо указать ссылку на свой плейлист из ЛК iedem
url = 'http://iedem.tv/playlists/uplist/your_id/playlist.m3u8'
playlist = get(url)

playlist_list = []
json_list = []

playlist.encoding = 'utf-8'
for playlist_line in playlist.text.split('\n'):
    playlist_list.append(playlist_line.strip('\r'))

for playlist_line_2 in playlist_list:
    if '#EXTINF' in playlist_line_2:
        json_list.append(playlist_line_2.split(',')[1].strip())

with open('channels_sorted.txt', 'w', encoding='utf-8') as f:
    for k in sorted(json_list):
        f.write(k + '\n')
