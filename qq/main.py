#!/usr/bin/python
import json
import os
import urllib.request
import requests

# 下载歌曲并且设置参数
from base import set_mp3_info, xstr, init_folder, check_base_path

base_url = "http://39.98.194.220:3300"


def download_item(count, song_url, name, pic, artist, album, savePath):
    if song_url is None or name is None:
        print(name, '该资源不存在')
        return
    # 歌曲名 包含路径符号
    name = name.replace('\\', '＼')
    file_name, ext = os.path.splitext(str(song_url).split("?")[0])
    # 保存的文件地址
    file_path = os.path.join(savePath, name + ext)
    if os.path.exists(file_path):
        print(name + " 已存在 -- " + count)
        return
    # 下载mp3
    urllib.request.urlretrieve(song_url, file_path)
    # 图片流文件
    info = {'pic': requests.get(pic).content,
            'title': name,
            'artist': artist,
            'album': album}
    set_mp3_info(count, file_path, info)


# 获取歌曲信息
def build_song_info(song, count, save_path, cookie):
    # 专辑封面
    album_cover = "https://y.gtimg.cn/music/photo_new/T002R300x300M000{}.jpg".format(song["albummid"])
    # 获取下载连接
    url = "{}/song/url?id={}&mediaId={}&type={}&ownCookie=1".format(base_url, song["songmid"], song["strMediaMid"],
                                                                    "320")
    json = requests.get(url, cookies=cookie).json()
    mp3_url = json.get("data")
    download_item(str(count), mp3_url, song["songname"], album_cover, song["singer"][0]["name"],
                  song["albumname"], save_path)


# 获取歌单信息
def songlist_info(song_id, save_path, cookie):
    url = "{}/songlist?id={}&ownCookie=1".format(base_url, song_id)
    r = requests.get(url, cookies=cookie)
    json = r.json()
    data = json.get("data")
    dissname = data["dissname"]
    print("歌单名称：" + dissname)
    print("歌单描述：" + xstr(data["desc"]))
    print("歌单封面：" + data["logo"])
    print("歌曲数量：" + str(data["songnum"]))
    songlist = data["songlist"]
    count = 0
    save_path = os.path.join(save_path, dissname)
    # 创建文件夹
    init_folder(save_path)
    for song in songlist:
        count = count + 1
        try:
            build_song_info(song, count, save_path, cookie)
        except Exception as e:
            print(e)
            print("歌曲id:{},歌曲名称:{},发生异常，联系管理员q：872019874".format(song_id, song["songname"]))
            continue


def get_config():
    with open('qq_music_config.json', 'r') as f:
        data = json.load(f)
    return data.get("base_path"), data.get("playId"), data.get("cookie")


if __name__ == '__main__':
    (save_path, song_id, cookie_str) = get_config()
    for param in (save_path, song_id, cookie_str):
        assert '<' not in param, '请设置参数：' + param
    cookie = {"cookie": cookie_str}
    # 最后需要加上 '/'
    save_path = check_base_path(save_path)
    init_folder(save_path)
    # 开始程序
    print("歌单id：{} ---开始下载---".format(song_id))
    songlist_info(song_id, save_path, cookie)
    print("歌单id：{} ---结束下载---".format(song_id))
