#!/usr/bin/python
import os
import time
import sys
import urllib.request

import requests
from pydub import AudioSegment
import json

from base import set_mp3_info, init_folder, xstr, check_base_path

# 不需要动
base_url = "http://39.98.194.220:3000"


# 获取歌曲url
def get_songsurl(songid, cookies, songs_map):
    url = "{}/song/url?id={}&timestamp={}".format(base_url, songid, str(int(round(time.time() * 1000))))
    r = requests.get(url, cookies=cookies)
    songs_url_data = r.json().get("data")
    for song in songs_url_data:
        song_url = song.get("url")
        songs_map[song["id"]] = {"url": song_url}


# 获取歌曲的 名称，歌手，专辑，专辑封面
def get_songs_info(songs_map, songids):
    url = "{}/song/detail?ids={}&timestamp={}".format(base_url, songids, str(int(round(time.time() * 1000))))
    data = requests.get(url).json()
    songs_data = data.get("songs")
    for song in songs_data:
        name = song['name']
        artist = song["ar"][0]["name"]
        album = song["al"]["name"]
        pic = song["al"]["picUrl"]
        # 取出值 然后再赋值
        song_tmp = songs_map[song["id"]]
        song_tmp['name'] = name
        song_tmp['artist'] = artist
        song_tmp['album'] = album
        song_tmp['pic'] = pic
        songs_map[song.get("id")] = song_tmp


# 网络下载文件
def download_item(count, url, name, pic, artist, album, save_path):
    if url is None or name is None:
        print(name, '该资源不存在')
        return
    name = name.replace('/', '／').replace('\\', '＼')
    file_name, ext = os.path.splitext(url)
    # 获取文件地址
    file_path = os.path.join(save_path, name + ext)
    mp3_file_path = os.path.join(save_path, name + ".mp3")
    if os.path.exists(mp3_file_path):
        print(name + " 已存在 -- " + count)
        return

    # 下载歌曲文件
    urllib.request.urlretrieve(url, file_path)
    # 不是mp3 将其转换成mp3
    if ext != '.mp3':
        audio = AudioSegment.from_file(file_path)
        audio.export(mp3_file_path, format="mp3")
        # 删除其他格式源文件
        os.remove(file_path)
        file_path = mp3_file_path

    # 图片流文件
    r = requests.get(pic)
    info = {'pic': r.content,
            'title': name,
            'artist': artist,
            'album': album}
    set_mp3_info(count, file_path, info)


# 循环下载
def download(savePath, songsMap):
    init_folder(savePath)
    count = 0
    os.chdir(savePath)
    for (key, song) in songsMap.items():
        url = song.get("url")
        name = song.get("name")
        pic = song.get("pic")
        artist = song.get("artist")
        album = song.get("album")
        # 下载文件并且设置
        count = count + 1
        download_item(str(count), url, name, pic, artist, album, savePath)


# 获取歌单中歌曲ids
def get_songsid(playid, cookies, param_map):
    try:
        url = "{}/playlist/detail?id={}&timestamp={}".format(base_url, playid, str(int(round(time.time() * 1000))))
        r = requests.get(url, cookies=cookies)
        playList = r.json().get("playlist")
        trackIds = playList.get("trackIds")
        print("专辑封面：" + playList.get("coverImgUrl"))
        albumName = playList.get("name")
        # 歌单名称放入变量中
        param_map['albumName'] = albumName
        print("专辑名称：" + albumName)
        print("专辑描述：" + xstr(playList.get("description")))
        print("歌曲数量：" + str(len(trackIds)))
        list_new = map(lambda x: str(x.get("id")), trackIds)
        if len(trackIds) == 0 or not list_new:
            print("该歌单为空！歌单名称：" + albumName)
            sys.exit()
        else:
            return ",".join(list_new)
    except AttributeError:
        print("歌单不存在～～")
        sys.exit()


# 获取配置
def get_config():
    with open('net_music_config.json', 'r') as f:
        data = json.load(f)
    return data.get("base_path"), data.get("playId"), data.get("token")


if __name__ == '__main__':
    # 配置信息
    (base_path, playId, token) = get_config()
    for param in (base_path, playId, token):
        assert '<' not in param, '请设置参数：' + param
    # 最后没有 / 的要加上
    base_path = check_base_path(base_path)
    param_map = {}
    cookies = {"MUSIC_U": token}
    # 获取歌单中歌曲ids
    song_ids = get_songsid(playId, cookies, param_map)
    # key歌曲id，val歌曲信息
    songs_map = {}
    # 填充歌曲下载地址
    get_songsurl(song_ids, cookies, songs_map)
    # 获取歌曲信息(专辑封面)
    get_songs_info(songs_map, song_ids)
    # 下载文件并且设置参数
    save_path = base_path + param_map["albumName"]
    print("开始下载")
    download(save_path, songs_map)
    print("下载完成！")
