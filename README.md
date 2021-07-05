## Forked from https://gitee.com/kidKing/music

## 将歌单下载，并且导入Apple Music

### 介绍

> 网易云下载歌单基于项目：https://github.com/Binaryify/NeteaseCloudMusicApi.git
>
> QQ音乐下载歌单基于项目：https://github.com/jsososo/QQMusicApi.git
>
> 在此致敬～

### 准备工作

- 安装依赖文件

```python
pip3 install -r requirements.txt
```

- 填写配置信息
1. base_path:保存路径（Mac用户尽量不要保存在桌面，桌面会上传iCloud，占用网速）
2. playId:歌单id（下面会介绍如何获取）
3. token/cookie:用户凭证（下面会介绍如何获取）



### 网易云

#### playId



![image-20210705112729403](https://picbed.kid510.com/picGo/20210705112729.png)



复制链接，红框中就是



![image-20210705112538990](https://picbed.kid510.com/picGo/20210705112601.png)



#### token

登陆网页版的网易云，F12查看-->Application-->Cookie-->Music_U



![image-20210705113726270](https://picbed.kid510.com/picGo/20210705113726.png)





### QQ音乐

#### playId



![image-20210705113513628](https://picbed.kid510.com/picGo/20210705113513.png)



浏览器打开，查看地址栏即可获取



![image-20210705113551668](https://picbed.kid510.com/picGo/20210705113551.png)





#### cookie



![image-20210705115934536](https://picbed.kid510.com/picGo/20210705115934.png)



### 执行程序



qq音乐为例：

进入 music/qq 目录执行

```python
python3 main.py
