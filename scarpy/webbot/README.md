Webbot用户手册
==============

## 爬虫列表

- example(通用型)
- jsonbot(通用型)

> 注意: 除此之外的爬虫, 已被废弃(或, 在开发中)!

## 功能列表

- config(json)
- xpath(ver1.0+extensions)
- regex(python flavor)
- macro(year/month/day/hour/minute/second)
- page(start/stop/step)
- parse(int/float/date/utc/text/map)
- plugin(python script)
- filter(detetime-delta/regex/number-range)
- database(mongo[automatically]/mysql[manually])
- proxy(http/https/socks4/socks5)
- HttpMethod(GET/POST)
- HttpHeader(Cookie/Usage-Agent/Referer)
- logging(DEBUG/INFO/WARNING/ERROR)
- settings(`download_timeout/download_delay/user_agent`)
- MessageQueue(zmq)
- StatsPost
- BatchDeploy
- debug

## scrapy入门

- test:

        $ scrapy crawl <spider>
        
- deploy:

        $ scrapy deploy <project>
        
- schedule:

        $ curl http://yourdomain:6800/schedule.json -d project=<project> -d spider=<spider> -d config=</path/to/spider.conf> -d setting=DOWNLOAD_DELAY=1
        
- cancel:

        $ curl http://yourdomain:6800/cancel.json   -d project=<project> -d job=xxxxxxxxxxx
        
- listjobs:

        $ curl http://yourdomain:6800/listjobs.json -d project=<project>

## 在线工具

- http://yourdomain:6800/
- http://jsonlint.com/
- http://regexpal.com/
- http://dillinger.io/

## Firefox插件

- https://addons.mozilla.org/en-US/firefox/addon/firebug/
- https://addons.mozilla.org/en-US/firefox/addon/firepath/
- https://addons.mozilla.org/en-US/firefox/addon/firequery/
- https://addons.mozilla.org/en-US/firefox/addon/imacros-for-firefox/


配置文件语法
============

本文描述了webbot配置文件的语法规范. 详情参考[schema.json](http://192.168.3.175/schema.json).

## site

**站点名称**, 值类型为`字符串`, 默认值为`"未知站点"`. 例如:

    "天涯论坛"

站点名称, 需要简明扼要, 并且能够精确描述本配置文件的用途.

## domains

**站点域名**, 值类型为`数组`, 默认值为`[]`(即, 空数组). 例如:

    ["bj.news.site.com", "sh.news.site.com"]

爬虫在提取页面中链接时, 会自动忽略除此之外的域名. 例如, 上述配置会忽略下述链接:

    "http://tj.news.site.com"
    "http://www.ads.com"

## urls

**入口链接**, 值类型为`数组`或`字典`, 默认值为`[]`(即, 空数组). 例如:

    [
        "http://www.site.com/?rn=10&cate=%B5%D8%C7%F8&city=北京",
        "http://www.site.com/?rn=10&cate=%B5%D8%C7%F8&city=上海",
        "http://www.site.com/?rn=10&cate=%B5%D8%C7%F8&city=广州",
        "http://www.site.com/?rn=10&cate=%B5%D8%C7%F8&city=重庆",
        "http://www.site.com/?rn=10&cate=%B5%D8%C7%F8&city=天津"
    ]

当这些链接具有共同特征时, 可以使用规则自动生成. 例如:

    {
        "base": "http://www.site.com/?rn=10",
        "qstr": {
            "type": 1,
            "cate": {"val":"地区", "enc":"gbk"}
        },
        "keywords": {
            "name": "city",
            "file": "http://www.mysite.com/cities.txt",
            "list": ["北京", "上海"],
            "enc" : "utf-8"
        },
        "method": "GET"
    }

- `base`: 基础链接(可以含有查询字段), 值类型为`字符串`.
- `qstr`: 链接的查询部分, 值类型为`字典`. 用来描述固定查询字段.
- `keywords`: 关键词, 值类型为`字典`. 用来描述动态查询字段.

    * `name`: 关键词名称, 值类型为`字符串`, 不能为空.
    * `file`: 文件名称, 值类型为`字符串`. 可以使用本地或网络路径, 编码方式必须是`UTF-8`.

            # http://www.mysite.com/cities.txt
            广州
            重庆
            天津

    * `list`: 关键词列表, 值类型为`数组`, 默认值为`[]`.
    * `enc`: 编码方式, 值类型为`字符串`, 默认值为`utf-8`. 可以对关键词进行编码.
    * `query`: 是否属于查询字段, 默认值为`true`. 当其值为`false`时, 会对基础链接进行替换.

            {
                "base": "http://www.site.com/FORUM/index.html",
                "keywords": {
                    "name" : "FORUM",
                    "list" : ["news", "blog", "about"],
                    "query": false
                }
            }
            
            上述配置可以生成下述链接
            
            http://www.site.com/news/index.html
            http://www.site.com/blog/index.html
            http://www.site.com/about/index.html

- `pages`: 自动翻页(当且仅当`rules`为空时, 该配置才有效). 例如:

        {
            "xpath" : "//div[@id='page']",
            "regex" : "&(pn)=([0-9]+)",
            "start" : 1,
            "stop"  : 5,
            "group" : 2
        }

- `method`: HTTP请求方法, 值类型为`字符串`, 默认值为`GET`. 当其值为`POST`时, 可以模拟表单提交.
- `headers`: HTTP请求头, 值类型为`字典`, 默认值为`{}`. 不区分键的大小写. 例如:

        {
            "User-Agent": "webbot++(by kev++)",
            "Cookie": "hello=world; foo=bar"
        }

## rules

**链接规则集**, 值类型为`字典`, 默认值为`{}`(即, 空字典). 用来提取页面中满足条件的链接. 例如:

    {
        "#1": {
            "follow": true,
            "regex" : "/f\\?kw=",
            "xpath" : "//div[@class='sub_dir_box']"
        },
        "#2": {
            "follow": true,
            "regex" : "/f/fdir.*&pn=([0-9]+)",
            "xpath" : "//div[@class='pagination']/a[last()-1]",
            "pages" : {"start":1, "stop":5}
        },
        "#3": {
            "follow": true,
            "regex" : "&pn=([0-9]+)",
            "xpath" : "//div[@id='frs_list_pager']/a[@class='next']",
            "pages" : {"start":0, "stop":250}
        },
        "#4": {
            "follow": false,
            "regex" : "/p/[0-9]+",
            "xpath" : "//ul[@id='thread_list']//a[@class='j_th_tit']"
        }
    }

> 注意: 当`rules`为空时, 会直接下载`urls`中的所有链接, 也会按`keywords.pages`中的规则进行翻页, 并且按`fields`中的规则对页面进行解析.

**链接规则集** 是由**链接规则项**构成的. 其中， `#1`, `#2` ... `#4`为**规则项**序号(名称), 需要注意的是:

- 规则名称可以是任何不重复的字符串
- 这些规则不存在先后次序
- 它们会在每个页面中起作用
- 一个页面可能会同时匹配多条规则

**规则项**的值类型为`字典`, 由下列元素组成:

- `follow`, 是否跟踪链接, 值类型为`布尔`, 默认值为`true`.
    * 有且仅有一条规则项不跟踪链接(即, 值设为`false`), 表示在此链接所指向的页面中, 提取所需字段(参考**fields**)
- `regex`, 链接需要匹配的regex, 值类型为`字符串`, 默认值为`null`.
- `xpath`, 链接需要匹配的xpath, 值类型为`字符串`, 默认值为`null`. 在xpath中可以使用下列扩展函数:
    * datetime-delta(dt, tz, delta)
    * unixtime-delta(dt, delta)
- `sub`, 链接转换, 值类型为`字典`, 默认值为`null`. (先于`pages`执行)
    * `from`, 原始地址(转换前), 值类型为`字符串`, 不能为空.
    * `to`, 目标地址(转换后), 值类型为`字符串`, 不能为空.
- `pages`, 提取链接中的页码(数字), 判断是否在范围之内, 值类型为`字典`, 默认值为`null`. (需要同时设置上述的`regex`)
    * `start`, 起始页码(包含), 值类型为`整数`, 默认值为`1`.
    * `stop`, 终止页面(不包含), 值类型为`整数`, 默认值为`5`.
    * `group`, 需要提取的`regex`分组编号, 值类型为`整数`, 默认值为`1`.

> 注意: `regex`, `xpath`, `pages`都是用来对链接进行过滤的, 需要同时满足.

## loop

**循环表达式**, 值类型为`字符串`, 默认值为`(//*)[1]`(即, root元素). 用该XPATH表达式来循环提取页面中多条信息. 例如:

    "loop": "//table/tr"

## fields

**字段定义**, 值类型为`字典`, 默认值为`{}`. 例如:

    {                                                                                     
        "url"     : {"name": "url",         "value": "${URL}"},
        "title"   : {"name": "title",       "xpath": "//h1[@id='title']/text()", "default": "未知标题"},
        "date"    : {"name": "ctime",       "xpath": "//div[contains(@class, 'l_post')][1]/@data-field", "parse": [{"type":"jpath", "query":"$.content.date"}, {"type":"cst"}]},
        "updated" : {"name": "gtime",       "value": "${NOW}", "parse": {"type": "date", "tz": "+08:00"}},
        "content" : {"name": "content",     "xpath": "//div[@class='d_post_content']", "parse": {"type":"text"}},
        "clicks"  : {"name": "visitCount",  "value": 0},
        "category": {"name": "info_flag",   "value": "02"}
    }

上述对字段的定义, 可以提取网页中的下述信息:

     category : 02
      updated : 2013-04-23 15:15:09
          url : http://news.qq.com/a/20130423/000484.htm
        title : 俄海军重型巡洋舰“瓦良格”号将远航访问亚太
      content : 中新社莫斯科4月22日电 (记者 贾靖峰)俄罗斯海军太平洋舰...
         date : 2013-04-23 01:06:00
       clicks : 0

**字段定义集**, 是由多个 **字段定义项**组成. 每个**字段定义项**由`字段名称`(值类型为`字符串`)和`字段定义`(值类型为`字典`)组成.
其中, `字段定义`由下列元素组成:

- `name`, 数据库字段名称
    * 若无该字段, 则不会写入数据库, 并在**debug**模式下, 会在名称后打印`*`标识.
- `value`, 固定值, 取值范围为:
    * 整数
    * 浮点数
    * 字符串
- `xpath`, xpath表达式
- `default`, 默认值, 取值范围于`value`相同. 若`value`及`xpath`提取数据为空, 则使用该默认值.
- `regex`, regex表达式(先于`parse`执行)
- `parse`, 数据解析, 值类型为`字典`或`数组`(由`字典`组成), 默认值为`{}`.
    * 当值类型为`字典`时:
        - `type`, 解析类型, 值类型为`字符串`, 默认值为`str`. (取值范围为下述10+种之一):
            * `str`, 文本
            * `text`, 文本(自动去除tag)
            * `unesc`, HTML实体转义

                    # "hello&amp;world" => "hello&world"
                    {"type":"unesc"}

            * `clean`, 清理HTML(自动去除style/script/meta/links等)
            * `jpath`, jpath表达式
            * `sub`, 字符替换
                - `from`, 替换前
                - `to`, 替换后

                        # "hello - world"  => "world - hello"
                        {"type":"sub", "from":"(.*) - (.*)", "to":"\\g<2> - \\g<1>"}

            * `int`, 整数
            * `float`, 浮点数
            * `join`, 拼接
                - `sep`, 分隔符, 值类型为`字符串`, 默认值为`" "`(即, 空格).
            * `list`, 拼接(自动去除tag)
                - `sep`, 分隔符, 值类型为`字符串`, 默认值为`" "`(即, 空格).
            * `date`, 日期
                - `fmt`, 日期格式, 值类型为`字符串`, 默认值为`auto`. 可自动识别下列日期格式:
                    * 刚刚
                    * 几秒前
                    * 8秒前
                    * 8分钟前
                    * 8小时前
                    * 8天前
                    * 今天 12:12
                    * 昨天 12:12
                    * 前天 12:12
                    * 2013年3月5日 18:30
                    * 2013年03月05日 18:30
                    * 2013-03-05 18:30
                    * 2013-3-5 18:30:00
                    * ...
                - `tz`, 时区, 值类型为`字符串`, 默认值为`+00:00`(即, UTC时间). 注意: 当涉及到相对时间计算时, 需要指定`tz`.
            * `cst`, CST(China Standard Time)日期 (`{"type":"cst"}`等价于`{"type:"date", "tz":"+08:00"}`), 为中国大陆用户量身定做
                - `fmt`, 日期格式, 值类型为`字符串`, 默认值为`auto`.
            * `continue`, 继续解析. 解析结果必须是个url, 自动下载该url, 并继续解析:

                    {
                        "fields": {
                            "url": {"name":"url",       "value":"${URL}"},
                            "txt": {"name":"content",   "xpath":"//iframe[@id='content']/@src", "parse":{"type":"continue"}}
                        },

                        "continue": {
                            "fields": {
                                "txt": {"name":"content",   "xpath":"//div[@class='content']", "parse":{"type":"text"}}
                            }
                        }
                    }

    * 当值类型为`数组`时, 会按先后顺序, 依次进行数据变换. 例如:
    
            # 首先使用`jpath`提取字符串, 并指定它为`cst`时间
            [{"type":"jpath", "query":"$.content.date"}, {"type":"cst"}]

- `filter`, filter表达式(后于`parse`执行), 值类型为`字典`, 默认值为`{}`. 其中, 键取值范围如下:
    * `delta`, 最大时间差(单位: `秒`), 只能用于过滤`datetime`类型的字段(使用UTC时间进行比较)
    * `match`, 字符串匹配, 只能用于过滤`string`类型的字段
    * `min`, 最大数值, 只能用于过滤`number`类型的字段
    * `max`, 最小数值, 只能用于过滤`number`类型的字段

另外, **rules** 以及 **fields** 中的`value`及`xpath`中可以嵌入变量(形如, `${VARNAME}`), 目前支持下列变量:

    'UTCNOW':   utcnow.strftime('%Y-%m-%d %H:%M:%S'),
    'NOW':      now.strftime('%Y-%m-%d %H:%M:%S'),
    'TODAY':    now.strftime('%Y-%m-%d'),
    'ITODAY':   '%d-%d-%d'.format(now.year, now.month, now.day)

    'YEAR':     now.strftime('%Y'),
    'MONTH':    now.strftime('%m'),
    'DAY':      now.strftime('%d'),
    'HOUR':     now.strftime('%H'),
    'MINUTE':   now.strftime('%M'),
    'SECOND':   now.strftime('%S'),

    'IMONTH':   str(now.month),
    'IDAY':     str(now.day),
    'IHOUR':    str(now.hour),
    'IMINUTE':  str(now.minute),
    'ISECOND':  str(now.second),

    'UNOW':     str(int(time.time())),
    'UTODAY':   str(int(time.mktime(time.strptime(now.strftime('%Y-%m-%d'), '%Y-%m-%d')))),
    'UENDDAY':  str(int(time.mktime(time.strptime(now.strftime('%Y-%m-%d 23:59:59'), '%Y-%m-%d %H:%M:%S'))))
    
    'SITE':     站点名称, 于`site`值一致
    'CONF':     配置文件内容
    'URL':      本页面链接(仅用于**fields** 字段定义, 不可在**rules**中使用)

## proxy

**代理设置**, 值类型为`字典`. 例如:

    {
        "enabled" : true,
        "rate"    : 5,
        "file"    : "http://192.168.3.155/proxy.txt",
        "list"    : [
                      "http://1.2.3.4:5678",
                      "socks5://8.7.6.5:4321"
                    ]
    }

由下列元素组成:

- `enabled`, 是否生效, 值类型为`布尔`, 默认值为`true`.
- `rate`, 代理变化频率, 值类型为`整数`, 默认值为`10`(表示: 每10次HTTP请求, 就随机切换代理).
- `file`, 代理列表文件, 值类型为`字符串`, 可以使用本地或网络路径, 编码方式必须是`UTF-8`.

        # 由3个字段组成(prot/host/port), 它们之间用空白符(如, `tab`)分隔
        http    218.29.218.10   6666
        http    122.96.59.103   80
        http    61.136.93.38    8080

- `list`, 固定代理列表, 值类型为`数组`, 默认值为`[]`, 由形如`prot://host:port`的代理地址组成:
    * `prot`, 协议类型, 如`http`, `https`, `socks5`, `socks4`等(只支持`http`)
    * `host`, 主机名(或IP地址)
    * `port`, 端口号

## debug

**调试模式**, 值类型为`布尔`, 默认值为`false`. 当值为`true`时, 程序运行过程中, 会把采集到的item详情输出到屏幕.

## settings

**全局设置**, 值类型为`字典`, 默认值为`{}`. 控制爬虫特定行为. 例如:

    {
        "user_agent": "Mozilla 5.0 (webbot by Kev++)",
        "download_timeout": 30,
        "download_delay": 5,
        "plugin: "/home/spider/configs/plugins/foobar.py",
        "mysql": "mysql://user:passwd@hostname/db_name.table_name"
    }
    
    - `user_agent`, 浏览器型号
    - `download_timeout`, 下载超时, 默认值为`30`(单位:秒)
    - `download_delay`, 两次下载之间的延时, 默认值为`0`(单位:秒)
    - `plugin`, 自定义插件, 仅支持python脚本(必需定义`parse`函数)
    - `mysql`, MySQL入库设置, 例如: `mysql://user:passwd@hostname:3306/db_name.table_name`
    - `mongo`, MongoDB入库设置, 例如: `mongodb://hostname:27017/db_name.collection_name`
    - `zmq`, ZeroMQ消息队列设置, 例如: `tcp://hostname:10086`

录入新的mysql库前, 需要根据**fields**, 创建相对应的`db_name`以及`table_name`.
参考SQL如下所示(请注意编码方式(`CHARSET`)):

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.sql}
    -- 建库
    CREATE DATABASE IF NOT EXISTS db_name DEFAULT CHARSET=utf8;
    
    -- 切换
    USE db_name

    -- 建表
    CREATE TABLE IF NOT EXISTS table_name
    (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        url VARCHAR(2084) NOT NULL,
        title TEXT NOT NULL,
        source TINYTEXT NOT NULL,
        siteName TINYTEXT NOT NULL,
        ctime DATETIME NOT NULL,
        gtime DATETIME NOT NULL,
        visitCount INT NOT NULL DEFAULT 0,
        replyCount INT NOT NULL DEFAULT 0,
        content MEDIUMTEXT NOT NULL,
        info_flag VARCHAR(10) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


配置Ubuntu服务器
================

## 安装系统

- Ubuntu 12.04.2 LTS
- OpenSSH Server
- Samba File Server

## 系统设置

    # 配置默认编辑器
    $ sudo update-alternatives --config editor
    
    # 配置系统时区
    $ sudo dpkg-reconfigure tzdata
    
    # 改主机名
    $ sudo vi /etc/host{s,name}
    $ sudo hostname ubuntuXXX

    # 添加新用户
    $ sudo adduser spider
    
    # 添加用户到组
    $ sudo adduser spider sudo
    
    # 切换用户
    $ sudo su spider
    
    # 改/etc/sudo文件
    $ sudo visudo
    
        # Allow members of group sudo to execute any command
        %sudo ALL=(ALL:ALL) NOPASSWD: ALL

    # 配置SSH(可选)
    $ ssh-copy-id spider@192.168.3.200

    # 下载tmux配置(可选)
    $ wget https://github.com/gotovoid/dot/raw/master/_tmux.conf -O ~/.tmux.conf

## 安装软件

    # 同步文件夹
    sudo chmod a+w /var/cache/apt/archives
    rsync --exclude='partial/' --include='*/' --include='*.deb' --exclude='*' -avz spider@192.168.3.195:/var/cache/apt/archives /var/cache/apt
    
    # 添加更新源
    if ! grep -q 'scrapy' /etc/apt/sources.list
    then
        echo 'deb http://archive.scrapy.org/ubuntu precise main' | sudo tee -a /etc/apt/sources.list
        curl -s http://archive.scrapy.org/ubuntu/archive.key | sudo apt-key add -
    fi
    
    # 安装软件
    sudo apt-get update
    sudo apt-get install -y scrapy-0.18 scrapyd python-pip python-zmq
    
    # 安装软件包
    PKGS=(pip pymongo pymysql redis jsonpath jinja2)
    sudo pip install --no-index --find-links=http://192.168.3.195/.pip/cache/ --upgrade ${PKGS[@]}

## 配置软件

    # 配置scrapyd
    $ sudo vi /etc/scrapyd/conf.d/000-default

        [scrapyd]
        http_port  = 6800
        debug      = off
        eggs_dir   = /var/lib/scrapyd/eggs
        dbs_dir    = /var/lib/scrapyd/dbs
        items_dir  =
        logs_dir   = /var/log/scrapyd
        jobs_to_keep = 20000
        max_proc_per_cpu = 5

    $ sudo service scrapyd restart

    # 配置mongodb
    $ sudo vi /etc/mongodb.conf

        bind_ip = 0.0.0.0

    $ sudo service mongodb restart

## 目录结构

    $ mkdir -p ~/configs/{log,keywords,bbs,blog,mblog,news}
    $ tree ~/configs
    
    configs/
    ├── README.md
    ├── log
    │   ├── webbot
    │   │   ├── index.html
    │   │   ├── config.html
    │   │   └── task.html
    │   └── twistd
    │       ├── twistd.log
    │       ├── twistd.log.1
    │       └── twistd.log.2
    ├── keywords
    │   ├── b1.dic
    │   ├── b2.dic
    │   └── b3.dic
    ├── bbs
    │   ├── abc_bbs.conf
    │   ├── def_bbs.conf
    │   └── ghi_bbs.conf
    ├── blog
    │   ├── abc_blog.conf
    │   ├── def_blog.conf
    │   └── ghi_blog.conf
    ├── mblog
    │   ├── abc_mblog.conf
    │   ├── def_mblog.conf
    │   └── ghi_mblog.conf
    └── news
        ├── abc_news.conf
        ├── def_news.conf
        └── ghi_news.conf

## 命名规则

        域名            配置名
    ------------    ------------
    bbs.abc.com     abc_bbc.conf
    blog.def.org    def_blog.conf
    news.ghi.net    ghi_news.conf

## WEB服务

    $ sudo vi /etc/rc.local

    # rc.local
    /usr/bin/twistd web --port=80 --path=/home/spider/configs --mime-type=text/plain --logfile=/home/spider/configs/log/twistd.log
    exit 0

## 计划任务

    $ crontab -e

    # m h  dom mon dow   command
    ################################## NEWS ########################################
    15 */1 * * * curl http://192.168.3.154:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=3600 -d config=http://192.168.3.155/news/abc_news.conf
    ################################## BLOG ########################################
    15 */7 * * * curl http://192.168.3.154:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=3600 -d config=http://192.168.3.155/news/abc_blog.conf
    ################################## BBS ########################################
    15 */3 * * * curl http://192.168.3.154:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=3600 -d config=http://192.168.3.155/news/abc_bbs.conf
    ################################## MBLOG ########################################
    15 */2 * * * curl http://192.168.3.154:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=3600 -d config=http://192.168.3.155/news/abc_mblog.conf

