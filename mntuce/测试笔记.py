# from fake_useragent import UserAgent
import rich

# ua = UserAgent(os='Windows')
# print(ua.chrome)

import os, re
from pathlib import Path
os.chdir(os.path.dirname(__file__))

# 1. 看看总共有多少照片
# count = 0
# for path in Path('./temp').iterdir():
#     p = re.search(r'\[(\d+).\]', path.name)
#     if p:
#         p = p.group(1)
#         count += int(p)
# print(count) # 3838

# 2.查看少了哪些, 应该是3838 + 69，69表示album封面照片
# count = 0
# for album_path in Path('./temp').iterdir():
#     raw_a = set(range(1, int(album_path.name[-4:-2]) + 2))
#     a = []
#     for photo_path in Path('./images/果儿Victoria').iterdir():
#         if album_path.name in photo_path.name:
#             number = re.search(r'_(\d+)\.jpg', photo_path.name).group(1)
#             a.append(int(number))
#     result = raw_a - set(a)
#     if len(result) != 0:
#         count += len(result)
#         print(album_path.name, str(result), album_path.read_text())
# print(count)


# father = Path('./images/果儿Victoria')

# albums = []
# for file in father.iterdir():
#     prefix_list = file.name.rsplit('_', 1)
#     if len(prefix_list) == 2:
#         if prefix_list[0] not in albums:
#             albums.append(prefix_list[0])
# # print(len(albums))
# # print(albums)

# raw_albums = os.listdir('./temp')
# a = (set(raw_albums) - set(albums))
# with open(f'./temp/{a.pop()}') as f:
#     print(f.read())


# 4. 解决失败重定向问题
# https://www.mntuce.com/37/.html
# import requests
# url = 'https://www.mntuce.com/37/.html'
# proxy = 'http://127.0.0.1:7897'
# proxy = {'http': proxy, 'https': proxy}
# r = requests.get()

# a = {"1", '2','3'}
# b = list(a)
# b.sort()
# print(','.join(a))
# print(','.join(b))

# from rich.console import Console
# import traceback
# # console = Console()
# # from rich import traceback

# def main():
#     try:
#         a = 3 / 0
#     except Exception as e:
#         # print(e)
#         # traceback.print_exc()
#         console.print_exception(show_locals=True)

# main()

# from rich.traceback import install
# install(show_locals=True)
# a = 3 / 0

import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    # handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)] # 只有rich_tracebacks=True时，后面一个参数才会生效
    handlers=[RichHandler(rich_tracebacks=False, tracebacks_show_locals=True)]
)

log = logging.getLogger("rich")
try:
    print(1 / 0)
except Exception:
    log.exception("unable print!")