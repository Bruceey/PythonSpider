# Scrapy-redis爬取美榜整站高清美女图片

该项目主要用于学习scrapy框架，涉及技术点有**图片文件的下载**、**请求头中间件**、**代理池中间件**、**scrapy转为scrapy-redis分布式**等技术要点的配置和重写。

目标网站首页：http://www.meibang88.com/mote/

目标网站基本没有反爬措施，但下载图片过于耗时，故采用分布式爬取，这样可以随时中断运行，再次启动便可从上次爬取的位置继续爬取。

### **1、技术架构**
(1) scrapy、scrapy-redis异步爬虫框架

(2) redis

(3) 代理池(非必须，利用github开源代理池修改)


### **2、相关环境安装**
(1) 安装redis

(2) 相关库的安装 

pip install -r requirements.txt

(3) 代理池的配置(非必须)

可以单独创建一个虚拟环境，例如可以打开conda终端创建proxy_pool虚拟环境，然后在此环境中pip install -r requirements.txt安装代理池需要的第三方库


### **3、运行**

(1) 首先运行start.py文件

(2) 打开redis的cli终端，输入 `lpush meibang:start_urls "http://www.meibang88.com/mote/"`

(3) 中断运行后，下次再启动start.py即可继续上次的位置爬取