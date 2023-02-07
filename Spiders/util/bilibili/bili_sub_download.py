import json
import os
import sys
import re
import shutil
import ssl
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from random import choice
import traceback


#设置请求头等参数，防止被反爬
headers = {
   'Accept': '*/*',
   'Accept-Language': 'en-US,en;q=0.5',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}

def get_user_agent():
   '''获取随机用户代理'''
   user_agents = [
       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
       "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
       "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
       "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
       "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
       "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
       "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
       "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
       "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
       "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
       "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
       "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
       "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
       "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
       "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
       "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
       "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
       "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
       "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
       "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
       "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
       "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
       "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36",
       "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20",
       "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
       "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）"
   ]
   # 在user_agent列表中随机产生一个代理，作为模拟的浏览器
   user_agent = choice(user_agents)
   headers = {
   'Accept': '*/*',
   'Accept-Language': 'en-US,en;q=0.5',
   'User-Agent': user_agent
    }
   return headers

def get_cid(bvid):
    cids = []
    names = []
    try:
        """得到cid"""
        header = get_user_agent()         
        # url = "https://api.bilibili.com/x/player/pagelist?aid={avid}&jsonp=jsonp".format(avid=avid)
        url = "https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp".format(bvid=bvid)
        response = requests.get(url,headers=header).json()
        #print(response)
        for data in response["data"]:
            cids.append(data["cid"])
            names.append(data["part"])
    except Exception as e:
        print(e)
    return cids ,names

def get_suburl(aid, cid):
    sub_url = ""
    try:
        url = "https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}".format(aid=aid, cid=cid)
        """获得视频真实flv地址"""
        header = get_user_agent()
        response = requests.get(url, headers=header).json()
        sub_url = "https:" + response["data"]["subtitle"]["subtitles"][0]["subtitle_url"]
        # 计算视频时长
        print('当前视频字幕地址: {}'.format(sub_url))
    except Exception as e:
        print(e)
        print('视频字幕地址获取失败')
    return sub_url

def get_sub(out_dir, sub_url, bvid, up_name):
    try:
        output_path = os.path.join(out_dir, up_name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        filename = f'{output_path}/{bvid}.txt'
        if os.path.exists(filename):
            return
        headers = get_user_agent()
        # 更新请求头
        response = requests.get(sub_url, headers=headers).json()
        sub_body = json.dumps(response["body"], ensure_ascii=False)
        print(sub_body)
        sub_file = open(filename, 'w')
        sub_file.write(sub_body)
         
    except Exception as e:
        print(e)
        print(f'视频下载失败')


def main02():
    # bvid = 'BV1cf4y137JG'
    #bvid = 'BV155411Y7gU'
    video_info_list = []
    input_path = sys.argv[1]
    out_dir = sys.argv[2]
    for i in open(input_path,"r",encoding="utf-8"):
        video_info = {}
        line = i.strip()
        up_name = line.split("\t")[0]
        bvid = line.split("\t")[1].split("/")[-1].split("?")[0]
        aid = line.split("\t")[2]
        video_info["up_name"] = up_name
        video_info["bvid"] = bvid
        video_info["aid"] = aid
        video_info_list.append(video_info)
    print(video_info_list)
    try :
        for video_info in video_info_list: 
            up_name = video_info["up_name"]
            bvid = video_info["bvid"]
            aid = video_info["aid"]
            cids, names = get_cid(bvid)
            #print(cid, name)
            for i,cid in enumerate(cids):
                sub_url = get_suburl(aid=aid, cid=cid)
                get_sub(out_dir, sub_url, bvid, up_name)
    except Exception as e:
        print (e)
        traceback.print_exc()


if __name__ == '__main__':
    # main(sys.argv[1:])
    # main01()
    main02()
