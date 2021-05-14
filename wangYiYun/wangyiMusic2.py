import requests
from fake_useragent import UserAgent
import json
from pprint import pprint
import base64

ua = UserAgent()
headers = {
    'User-Agent': ua.random,
}

comment_url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
data = {
    'params': 'MlFGIGxNPR9N7gu2GrKUye/R7NhuYHiXG7XrRlpOZrsv6FGd/iNJMcZS44wB5TRfNOd+3pBhNRzTjr68oC13Muj1we8Iw7QyES2qLZR+cI+orklzpHUrfM6o6FNl0vntOhSptmWyqSjEIXi1TONb995bjUNiu2pbn/RYfdDsw0iDcMBRe4JxTnV8f/EphUKZGd2EfWxSY4JCGSCuOJfuvIz4zQN1nIwvkxiGH3TbkZKydeYkEO2+sZoyn9JjNzWmf7y8ChjM9+nEkHsnXBwIJQ==',
    'enSecKey': 'bb365897090785c05beff75320d0edd0b89518941641c574cc6bc163ab602d38d824047bded72327b87a4dbd9ee0c91901567239a908381875063833f28a80e17607023c0e5d3927aebb10836538a8730fae5747dfc4333504671a448cbebe22d41a5026ebb5f36816108396f7b278df3957d7dbbd820441692123430e6127d1',
}

"""
加密过程
function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    window.asrsea = d,
    window.ecnonasr = e
"""

e = "010001"
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
