js = """
function f()
{
                        //if (!(this instanceof r))
                        //    return new r(arguments[0],arguments[1],arguments[2],arguments[3]).toString();
                        "object" == a(arguments[0]) ? (this.timestamp = arguments[0].timestamp,
                        this.machine = arguments[0].machine,
                        this.pid = arguments[0].pid,
                        this.increment = arguments[0].increment) : "string" == typeof arguments[0] && 24 == arguments[0].length ? (this.timestamp = Number("0x" + arguments[0].substr(0, 8)),
                        this.machine = Number("0x" + arguments[0].substr(8, 6)),
                        this.pid = Number("0x" + arguments[0].substr(14, 4)),
                        this.increment = Number("0x" + arguments[0].substr(18, 6))) : 4 == arguments.length && null != arguments[0] ? (this.timestamp = arguments[0],
                        this.machine = arguments[1],
                        this.pid = arguments[2],
                        this.increment = arguments[3]) : (this.timestamp = Math.floor((new Date).valueOf() / 1e3),
                        this.machine = o,
                        this.pid = t,
                        this.increment = e++,
                        e > 16777215 && (e = 0))
                    };

function getTraceId(){
    var oid = new f();
    oid.toString = function() {
                    if (void 0 === this.timestamp || void 0 === this.machine || void 0 === this.pid || void 0 === this.increment)
                        return "Invalid ObjectId";
                    var e = this.timestamp.toString(16)
                      , t = this.machine.toString(16)
                      , n = this.pid.toString(16)
                      , r = this.increment.toString(16);
                    return "00000000".substr(0, 8 - e.length) + e + "000000".substr(0, 6 - t.length) + t + "0000".substr(0, 4 - n.length) + n + "000000".substr(0, 6 - r.length) + r
                }
    return oid.toString()
}
"""


# import execjs
# ctx = execjs.compile(js)
# result = ctx.call('getTraceId')
# print(result)

"""
this.oid = {
increment: 7位整数, Math.floor(16777216 * Math.random()) + 1
machine: 7位整数,  Math.floor(16777216 * Math.random())
pid: 5位整数,  Math.floor(65536 * Math.random())
timestamp: 10位时间戳(即秒)   int(time.time())
}

var e = this.timestamp.toString(16)
                      , t = this.machine.toString(16)
                      , n = this.pid.toString(16)
                      , r = this.increment.toString(16);
                    return "00000000".substr(0, 8 - e.length) + e + "000000".substr(0, 6 - t.length) + t + "0000".substr(0, 4 - n.length) + n + "000000".substr(0, 6 - r.length) + r

"""
import time
import random
import requests

e = str(hex(int(time.time())))[2:]
t = str(hex(int(16777216 * random.random())))[2:]
n = str(hex(int(65536 * random.random())))[2:]
r = str(hex(int(16777216 * random.random())))[2:]

s = "00000000"[:8 - len(e)] + e + "000000"[:6 - len(t)] + t + "0000"[:4 - len(n)] + n + "000000"[:6 - len(r)] + r
ketracespiddtid = 'cq.fang.lianjia.com-' + s

headers = {
  # 'SSID': ' ca85434a-9c00-4624-92a0-1df238deebff',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
  # 'UUID': ' d97da4f3-2d1a-4bfa-b636-ee9ba16a023b',
  # 'X-Requested-With': ' XMLHttpRequest',
  'Referer': 'https://cq.fang.lianjia.com/',
  'ketracespiddtid': ketracespiddtid,
  # 'digv_extends': ' %7B%22utmTrackId%22%3A%22%22%7D'
}

url = 'https://ex.lianjia.com/sdk/recommend/html/100011051?hdicCityId=500000&id=100011051&mediumId=100000032&projectName=yhtyafryh&projectType=&elementId=tab-400&required400=true&parentSceneId='
r = requests.get(url, headers=headers)
print(r.text)