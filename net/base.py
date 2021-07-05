#!/usr/bin/python
import os
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB


# 设置mp3信息
def set_mp3_info(count, mp3file, info):
    try:
        song_file = ID3(mp3file)
        song_file['APIC'] = APIC(  # 插入封面
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc=u'Cover',
            data=info['pic']
        )
        song_file['TIT2'] = TIT2(  # 插入歌名
            encoding=3,
            text=info['title']
        )
        song_file['TPE1'] = TPE1(  # 插入第一演奏家、歌手、等
            encoding=3,
            text=info['artist']
        )
        song_file['TALB'] = TALB(  # 插入专辑名
            encoding=3,
            text=info['album']
        )
        song_file.save()
    except Exception as e:
        print(e)
        print(mp3file + "--发生异常 -- " + count)
    else:
        print(mp3file + "--处理完成 -- " + count)


# None的转为‘’
def xstr(s):
    return '' if s is None else str(s)


# 文件夹不存在，则创建文件夹
def init_folder(save_path):
    folder = os.path.exists(save_path)
    if not folder:
        os.makedirs(save_path)


# 保存路径如果 没有最后的 \\ 或者 / 添加上
def check_base_path(base_path):
    file_sep = os.sep
    base_path += file_sep if base_path[-1] != file_sep else ""
    return base_path
