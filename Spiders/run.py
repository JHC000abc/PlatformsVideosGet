# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     : 

"""
import requests
import time
import api
import datetime


def get_data(url,retry=3):
    flag=False
    response = ""
    while not flag and retry>0:
        try:
            response = requests.get(url)
            flag=True
        except:
            retry-=1
    return response

def write_error_log(msg):
    with open("./log.txt","a")as fp:
        fp.write("{}\n".format(msg))

while True:
    try:
        url = ""
        response = get_data(url)

        # 接口没数据，休眠半小时后再请求
        if response.status_code != 200:
            time.sleep(1800)
        # 接口书获取失败（重试三次）
        elif response.text == "":
            write_error_log("{} 数据获取异常".format(str(datetime.datetime.now())).split(".")[0])
        else:
            #   请求成功，数据获取到了
            if response.status_code == 200:
                data_json = response.json()
                for args in data_json:
                    api.ProcessInput(args)
                    time.sleep(1)

    except Exception as e:
        print(e,e.__traceback__.tb_lineno)



