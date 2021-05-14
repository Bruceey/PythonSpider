import requests
from urllib import parse
import json
import pandas as pd
import os
import time


def g_tk(skey):
    hash = 5381
    length = len(skey)
    for i in range(length):
        if i < length:
            hash += (hash << 5) + ord(skey[i])
    return 2147483647 & hash


page = 0

df_all = pd.DataFrame()

while True:
    comment_url = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    params = {
        # 'g_tk_new_20200303': g_tk("Q_H_L_2Ou6-160eWT0kjGauzHMtXeJETzw9dz7sEuZ-3rx4M2Mt3qowToV8PY0bK_XLLE"),
        'g_tk_new_20200303': '5381',
        # 'g_tk': g_tk("Q_H_L_2Ou6-160eWT0kjGauzHMtXeJETzw9dz7sEuZ-3rx4M2Mt3qowToV8PY0bK_XLLE"),
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'GB2312',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0',
        'cid': '205360772',
        'reqtype': '2',
        'biztype': '1',
        'topid': '97773',
        'cmd': '8',
        'needmusiccrit': '0',
        'pagenum': '0',
        'pagesize': '25',
        'lasthotcommentid': '',
        'domain': 'qq.com',
        'ct': '24',
        'cv': '10101010',
    }

    params = parse.urlencode(params)
    url = comment_url + params
    response = requests.get(url, headers=headers)
    result = response.text
    comment_info = json.loads(result)

    topid = comment_info['topid']
    topic_name = comment_info['topic_name']

    comment = comment_info['comment']
    comment_total = comment['commenttotal']
    comment_list = comment['commentlist']
    page_total = int((comment_total - 1) / 25) + 1

    if page >= 100:
        break

    for i in comment_list:

        comment_id = i['commentid']
        avatar_url = i['avatarurl']
        nick = i['nick']
        try:
            content = i['rootcommentcontent']
        except Exception as e:
            content = ''

        comment_time = i['time']
        timeArray = time.localtime(comment_time)
        comment_time = time.strftime("%Y年%m月%d日 %H:%M:%S", timeArray)

        praise_num = i['praisenum']
        vip_icon = i['vipicon']
        if vip_icon == '':
            vip_icon = '未开通会员'
        else:
            vip_icon = vip_icon[-9:-4]

        df = pd.DataFrame({
            '评论ID': comment_id,
            '头像链接': avatar_url,
            '昵称': nick,
            '评论内容': content,
            '评论时间': comment_time,
            '点赞数量': praise_num,
            '等级图标': vip_icon
        }, index=[0])
        df_all = df_all.append(df, ignore_index=True)

    page = page + 1
    time.sleep(1)
    print("第" + str(page) + "页内容获取完毕")

df_all.to_excel(os.getcwd() + "\\" + topic_name + '_' + str(comment_total) + '_最新评论.xlsx', index=False)