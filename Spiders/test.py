# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     : 

"""
import json

import requests


import requests


headers = {
    "Accept": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Origin": "https://v.youku.com",
    "Pragma": "no-cache",
    "Referer": "https://v.youku.com/v_show/id_XNDQwNjgxMTM2OA==.html?spm=a2hbt.13141534.1_3.1&s=a13661602b1a4f54bcd1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "xlly_s": "1",
    "cna": "tSZRHMjINn8BASQA2gAvRJSR",
    "__ysuid": "1675740054018ZCI",
    "__ayft": "1675740054022",
    "__aysid": "1675740054022rC8",
    "__ayscnt": "1",
    "__arycid": "dd-3-00",
    "__arcms": "dd-3-00",
    "_m_h5_tk": "d52bceda145114a6f2f902eef9798dd8_1675759291226",
    "_m_h5_tk_enc": "61cf490bd21ae6bc566320d34d040eec",
    "redMarkRead": "1",
    "P_ck_ctl": "A4C9A753504134FCA7A4C4E0C0BED53B",
    "__arpvid": "1675757013174emVpd6-1675757013197",
    "__aypstp": "14",
    "__ayspstp": "14",
    "__ayvstp": "62",
    "__aysvstp": "62",
    "tfstk": "c8xdBV9TNfch8CGlbM3gzVFYnVOdaj3dZff42nR475uLPWZYcsxpmnB_xlXAg6HO.",
    "l": "fBxziaF7T9sDVXWvBOfaFurza77OSIRYmuPzaNbMi9fP_-fw5PWRB6-22a8eC3GVFsMvR3PZC7jvBeYBqnbTXeQ21S0yReMmnmOk-Wf..",
    "isg": "BCkpAy6SbrrxoVIN-Fpp2j9dONWD9h0osLl1M8sepZBPkkmkE0Yt-BeEVDakDrVg"
}
url = "https://acs.youku.com/h5/mopen.youku.danmu.list/1.0/"
params = {
    "jsv": "2.7.0",
    "appKey": "24679788",
    "t": "1675757115747",
    "sign": "07356c7d219260def8c3ff34bdc45a6b",
    "api": "mopen.youku.danmu.list",
    "v": "1.0",
    "type": "originaljson",
    "dataType": "jsonp",
    "timeout": "20000",
    "jsonpIncPrefix": "utility"
}
data = {
    "data": "{\"pid\":0,\"ctype\":10004,\"sver\":\"3.1.0\",\"cver\":\"v1.0\",\"ctime\":1675757115723,\"guid\":\"tSZRHMjINn8BASQA2gAvRJSR\",\"vid\":\"XNDQwNjgxMTM2OA==\",\"mat\":13,\"mcount\":1,\"type\":1,\"msg\":\"eyJjdGltZSI6MTY3NTc1NzExNTcyMywiY3R5cGUiOjEwMDA0LCJjdmVyIjoidjEuMCIsImd1aWQiOiJ0U1pSSE1qSU5uOEJBU1FBMmdBdlJKU1IiLCJtYXQiOjEzLCJtY291bnQiOjEsInBpZCI6MCwic3ZlciI6IjMuMS4wIiwidHlwZSI6MSwidmlkIjoiWE5EUXdOamd4TVRNMk9BPT0ifQ==\",\"sign\":\"e9245847a3da21272b57716bf7049c2b\"}"
}
_set = set()
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)
response.encoding="utf-8"
for i in json.loads(json.loads(response.text)["data"]["result"])["data"]["result"]:
    _set.add(i["ouid"])

print(_set)
