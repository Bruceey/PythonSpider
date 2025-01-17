# 1. 常用设置解释
**注意媒体默认下载不是重定向的**
```python
IMAGES_STORE = "images"
MEDIA_ALLOW_REDIRECTS = True  # 打开媒体下载时允许重定向

LOG_FILE = 'xiuren.log'
# LOG_LEVEL = 'DEBUG'  # 设置为 'ERROR' 只会记录错误及更高级别的日志
LOG_FILE_APPEND = False # 设置日志是否追加，默认True追加
```

# 2. scrapy日志默认根logger是root，只能同时绑定1个handler，要么是FileHandler, 要么是StreamHandler
