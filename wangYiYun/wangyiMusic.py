import requests
from fake_useragent import UserAgent
import json
from pprint import pprint

ua = UserAgent()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'referer': 'https://music.163.com/song?id=190072',
    'cookie': '_ntes_nnid=8dcac18134f8c5732088c085ac7fba11,1597564309288; _ntes_nuid=8dcac18134f8c5732088c085ac7fba11; NMTID=00OgaLilXK7vWTCv0QkohVZtkLkzpgAAAF1P-wiSw; _iuqxldmzr_=32; WM_TID=k4OEXlBGI+VFQQBERQd6aJqk1vg0+Va2; __root_domain_v=.163.com; _qddaz=QD.3r4jnc.doev3e.klf2b135; OUTFOX_SEARCH_USER_ID_NCOO=1782830589.88964; hb_MA-BFF5-63705950A31C_source=study.163.com; UM_distinctid=1789ac3b636995-08fbc010902257-101a4459-1ea000-1789ac3b637c69; NTES_YD_SESS=Vlgs5BMRaSTqRxXaiG4kPKeFr1xWTYIyYfyo9iMD9bv0zSAkzfcxNLXJuwdyljHg2z56Jdm.xwSKPl6FMr1WVOUPkhbHdLvNRTuyNVfjFH_G2_SUtMxOLsFndKBMtkHSsU0VVJMMe5DcLVo_f2X3WhQvXuXdgdopSFohriQRp9CX_t3yHNF7NQPjkPJq4mwefIxlRL5w653c9AF7gUyIPs56tzU4n12GAiBeDjb6u9o.W; S_INFO=1617671471|0|3&80##|13512272329; P_INFO=13512272329|1617671471|0|study|00&99|zhj&1616932365&study#zhj&330100#10#0#0|&0|null|13512272329; NTES_CMT_USER_INFO=310518046|有态度网友0iwy4u|http://cms-bucket.nosdn.127.net/2018/08/13/078ea9f65d954410b62a52ac773875a1.jpeg|false|eWQuN2E5ODc3YTNmMDQxNGQ0YmJAMTYzLmNvbQ==; JSESSIONID-WYYY=Qw+0m1CXOchgdwh3mu3Z6nRhgcejy92CqzSkwmB+MZGSAHb4\sq009wydHdSiYo0vTNg\QGX/WqzIOcKVJG3akIFR35Z6lDxF9iRqx52OnxJxRR8lhGyv1IjyKNG6KS50M6+\b8/gUJkrZ1jIxpiO2Zv0pnAhdCO8mhk/HPianxsQW3h:1620035770084; WEVNSM=1.0.0; WM_NI=7DEF+xobqa+RKeYy9rH/iHfEhmhBvcsPGyLvdc+Ay4tAF0PTzmSOAdBb8NQmj9yRjvj38iEpnJRpz7BkzoPCh0eCZQEIc1PZiD52p1Tn2qvVvx39PYDowtTav9STvsO3YlM=; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb9e147f28b82b0ed668ce78fa3d15a878a8eafb568acac8889e1608a8d9cb3d52af0fea7c3b92af59c8ba7aa74adbebf82aa5a89bb979abc7a8cf1a7a9e54facb3a8a3f569b190899acf7ea8bde5a2fc40b89f8ad1d360bab39db0c47082bef8afd467aae7b7b3e97eaaedf88ac87cae969e91f93d82b5b690d349acf0aba4d95b8797add2d352ab9cfbd3f33b98b2fe92f55eb6a8fddad35388b1b995d76bb6e79db5f5798ded978dd037e2a3; playerid=85959114'
}

comment_url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
data = {
    'params': 'MlFGIGxNPR9N7gu2GrKUye/R7NhuYHiXG7XrRlpOZrsv6FGd/iNJMcZS44wB5TRfNOd+3pBhNRzTjr68oC13Muj1we8Iw7QyES2qLZR+cI+orklzpHUrfM6o6FNl0vntOhSptmWyqSjEIXi1TONb995bjUNiu2pbn/RYfdDsw0iDcMBRe4JxTnV8f/EphUKZGd2EfWxSY4JCGSCuOJfuvIz4zQN1nIwvkxiGH3TbkZKydeYkEO2+sZoyn9JjNzWmf7y8ChjM9+nEkHsnXBwIJQ==',
    'enSecKey': 'bb365897090785c05beff75320d0edd0b89518941641c574cc6bc163ab602d38d824047bded72327b87a4dbd9ee0c91901567239a908381875063833f28a80e17607023c0e5d3927aebb10836538a8730fae5747dfc4333504671a448cbebe22d41a5026ebb5f36816108396f7b278df3957d7dbbd820441692123430e6127d1',
}

r = requests.post(comment_url, headers=headers, data=data)
print(r.text)
# comment_data = json.loads(r.text)
# pprint(comment_data)