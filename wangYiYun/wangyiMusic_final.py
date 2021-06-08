# 1.找到未加密的参数        #通过函数window.asrsea()进行加密
# 2.想办法把参数进行加密，params--->encText  encSecKey--->encSecKey

from Crypto.Cipher import AES
from base64 import b64encode
import requests, json
from Crypto.Util.Padding import pad
from datetime import datetime
from pprint import pprint

e = "010001"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"
i = "CkkzndZixNU4CTCw"

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}


def get_encSecKey():
    return "d6b2ec2cd94402831d21131329525995a533160861d04a89289ccf5705d2586466c6f055bf643c4c1a95fd4efb0b7091e8e44d61f481a45634986674229d478536a7a2c854e333b244b9b7c40d318a6e92d2eabbb306135f599ef02a18850c4735ce813f86977c4e6ab21b87a9047da1fcf345f9eb7b8c79d29c740b3a12f3dd"


def get_params(data):  # data默认是json字符串
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second


def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def enc_params(data, key):  # 加密过程
    iv = "0102030405060708"
    # data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)  # 创建加密器
    pad_data = pad(data.encode('utf-8'), 16)
    bs = aes.encrypt(pad_data)  # 加密
    return str(b64encode(bs), "utf-8")  # 转化成字符串


# 处理加密过程
'''
 function a(a) { a=16
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length, #生成随机数
            e = Math.floor(e), #取整
            c += b.charAt(e); #取出b中对应位置的字符
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a) #e是数据
          , f = CryptoJS.AES.encrypt(e, c, { #c就是加密密钥 
            iv: d, #iv是偏移量
            mode: CryptoJS.mode.CBC # 模式：CBC加密
        });
        return f.toString()
    }
 一、
//setMaxDigits()貌似是生成密文的最大位数，如果不设置或者乱设置的话很可能导致死循环然后浏览器崩溃。
//这个语句必须最先执行，1024位的密钥要传入130,2048的话要传入260
setMaxDigits(130);
//RSAKeyPair是密钥对的对象，用e和n可以生成公钥，第二个参数其实就是d，因为我们只需要公钥当然是传空的。
key = new RSAKeyPair(e,"",n);
//下面是加密方法，比较简单，就是传入公钥和原文，加密成密文。
var result = encryptedString(key, document.getElementById("pwd").value);

二、
setMaxDigits()，到底应该传值多少？
在JS文件中给出公式为：n * 2 / 16。其中n为密钥长度。
    如果n为1024，则值应为 1024 * 2 / 16 = 128。

经过测试，传128后台解密会报错；正确的值应该大于128。

个人喜好的公式是：n * 2 / 16 + 3
即  密钥长度若为1024，其值为 131
    密钥长度若为2048，其值为 259
    
    
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) { d：数据json串  e:"010001" f:   g = "0CoJUm6Qyw8W8jud"
        var h = {}
          , i = a(16); #16位随机值
        return h.encText = b(d, g), g是密钥
        h.encText = b(h.encText, i), #返回的就是params i是密钥
        h.encSecKey = c(i, e, f), #返回的是encSecKey e和f定死，能产生变数的只能是i
        h
    }'''


def main():
    # page = int(input('请输入需要爬取的页数：'))
    page = 10
    print('开始爬虫！！！')
    fp = open('黄昏评论.txt', 'w', encoding='utf-8')
    for j in range(1, page + 1):
        data = {
            'csrf_token': "",
            'cursor': "-1",
            'offset': str((j - 1) * 20),
            'orderType': "1",
            'pageNo': str(j),
            'pageSize': '20',
            'rid': "R_SO_4_190072",
            'threadId': "R_SO_4_190072"
        }

        response = requests.post(url, data={
            "params": get_params(json.dumps(data)),
            "encSecKey": get_encSecKey()
        }, headers=headers)

        result = json.loads(response.content.decode('utf-8'))
        # hotComments
        hotComments = result['data']['hotComments']
        if hotComments:
            for hotComment in hotComments:
                fp.write('hotComments' + ' ')
                fp.write('昵称：' + hotComment['user']['nickname'] + '\n')
                fp.write('评论：' + hotComment['content'] + '\n')
                be_replied_comments = hotComment['beReplied']
                if be_replied_comments:
                    for be_replied_comment in be_replied_comments:
                        fp.write('回复者：' + be_replied_comment['user']['nickname'] + '\n')
                        fp.write('回复评论: ' + be_replied_comment['content'] + '\n')

                if hotComment['user']['vipRights']:
                    fp.write('vip:yes' + '\n')
                else:
                    fp.write('vip:no' + '\n')
                fp.write('点赞数' + str(hotComment['likedCount']) + '\n')
                time = int(hotComment['time']) / 1000
                time = datetime.fromtimestamp(time)
                time = time.strftime('%Y-%m-%d %H:%M:%S')
                fp.write("时间：" + time + '\n')
                fp.write('-------------------------------------' + '\n')

        # comments
        comments = result['data']['comments']
        for comment in comments:
            fp.write('comments')
            fp.write('昵称：' + comment['user']['nickname'] + '\n')
            fp.write('评论：' + comment['content'] + '\n')
            be_replied_comments = comment['beReplied']
            if be_replied_comments:
                for be_replied_comment in be_replied_comments:
                    fp.write('回复者：' + be_replied_comment['user']['nickname'] + '\n')
                    fp.write('回复评论: ' + be_replied_comment['content'] + '\n')

            if comment['user']['vipRights']:
                fp.write('vip:yes' + '\n')
            else:
                fp.write('vip:no' + '\n')
            fp.write('点赞数' + str(comment['likedCount']) + '\n')
            time = int(comment['time']) / 1000
            time = datetime.fromtimestamp(time)
            time = time.strftime('%Y-%m-%d %H:%M:%S')
            fp.write("时间：" + time + '\n')
            fp.write('-------------------------------------' + '\n')
    print('爬取完毕！！！')
    fp.close()


def main2():
    data = {
        'csrf_token': "",
        'cursor': "-1",
        'offset': "20",
        'orderType': "1",
        'pageNo': "2",
        'pageSize': '20',
        'rid': "R_SO_4_190072",
        'threadId': "R_SO_4_190072"
    }

    r = requests.post(url, data={
        "params": get_params(json.dumps(data)),
        "encSecKey": get_encSecKey()
    }, headers=headers)
    # comments = r.json().get('data').get('comments')
    # print(len(comments))
    # for k in comments:
    #     print(k.get('content'))
    pprint(r.json())


if __name__ == '__main__':
    main()
    # main2()
