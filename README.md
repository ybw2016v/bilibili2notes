# bilibili2notes

A python bot which can transfer bilibili dynamic to Misskey notes

一个用于搬运B站动态的Misskey机器人

-----

> Warn: The code may be uncomfortable , make sure that the emergency medicine is reachable before read the code.

> 警告:源代码可能会引起不适，在阅读前准备好降压药。

### 信息源

使用[RssHub](https://rsshub.app)作为B站动态的信息来源，如果RssHub主站连接不畅通可以更换其他RssHub站点，返回XML信息格式一致应该没问题。

### Information Source

The bilibili dynamic information is from [RssHub](https://rsshub.app) , which can return the bili dynamic in the xml format.Other website which can offer the information in the same format is also suitable.

More Information about RssHub and bilibili [https://docs.rsshub.app/social-media.html#bilibili](https://docs.rsshub.app/social-media.html#bilibili).

### 安装

1. 将`requests`升级到最新版本

``` bash
pip3 install requests --upgrade
```

2. 下载

```
git clone https://github.com/ybw2016v/bilibili2notes.git
```


### 使用方法

1. 将ini格式的配置文件放置在`conf`下

`conf`目录下可放置多个不同的配置文件，每个文件配置一个机器人。

配置文件说明

``` ini
[dog]
;机器人名称


PostUrl=https://example.com/
;Misskey实例url

SouUrl=https://rsshub.app/bilibili/user/dynamic/167446465
;信息源


ApiKey=Your ApiKey
;misskey机器人的apikey

Pex=
;Pex=机器人转发
;机器人发布前缀，无特殊需求留空

Afr=
;Afr=本条消息由机器人转发
;机器人发布后缀，无特殊需求留空

Extime=1209600
;设置图片的过期时间，超过1209600秒之后的过期图片将会被删除，以节约存储空间，如不清除历史图片，可设置为-1

```

2. 设置定时任务

``` bash
crontab -e
```

添加定时任务，RSShub的缓存时间大约为20分钟，设置执行间隔大于这个数应该不会出问题。

```
# m h  dom mon dow   command
30 * * * * cd /path/to/bilibili2notes && python3 bili2notes.py

```
每小时的第三十分钟会进行检查与更新。
### Install

1. Get the nearest version of `requests`

```bash
pip3 install requests --upgrade

```
2. Git Clone

```bash
git clone https://github.com/ybw2016v/bilibili2notes.git
```

### Usage

1. Put the configuration file to `conf`

More than one configuration files can be arranged in `conf`. Each configuration file control a different bot.



``` ini
[dog]
;Bot name


PostUrl=https://example.com/
;the url of misskey instance to post notes


SouUrl=https://rsshub.app/bilibili/user/dynamic/167446465
;Information Source

ApiKey=Your ApiKey
;apikey

Pex=
;Pex=From Bot
;The prefix of the notes which will be added to the front of notes,it might be null if  there is no special needs

Afr=
;The postfix of the notes which will be added to the end of notes,it might be null if  there is no special needs

Extime=1209600
;The time of image. All images which upload before this time (secend) will be deleted. Set -1 to disable this.

```

2. Set a timed task

``` bash
crontab -e
```

Add a task

```
# m h  dom mon dow   command
30 * * * * cd /path/to/bilibili2notes && python3 bili2notes.py

```
The script will run at 30 min in every hour.