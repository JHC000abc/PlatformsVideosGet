# !/usr/bin/env python3
import requests
import re
from random import choice
import time
import json
import os
import sys
import traceback
from setting import setting


def get_headers():
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
        'user-agent': user_agent,
        'cookie': 'ttwid=1%7CA-Z9dt_Wx-Qt3zXxiyBzlXFud7BfXIQ-w6Gw8xqERNg%7C1652168095%7C6f923634ba428157c83c3ba554db8ee56e94a216da9e2b2705159b6d0c94380f; _tea_utm_cache_2285=undefined; passport_csrf_token=b45487a9876b5084688f2b1f5ceb0930; passport_csrf_token_default=b45487a9876b5084688f2b1f5ceb0930; s_v_web_id=verify_l2zu8814_LmXRvNNe_saz6_45cc_AS36_JHKSsax3nrQM; AB_LOGIN_GUIDE_TIMESTAMP=1652168097947; AVATAR_LOGIN_GUIDE_COUNT=1; ttcid=c2dc734b05534a77ae77741b92660dc233; _tea_utm_cache_6383=undefined; _tea_utm_cache_1300=undefined; _tea_utm_cache_2018=undefined; AVATAR_FULL_LOGIN_GUIDE_ITA_TIMESTAMP=1652168365595; AVATAR_FULL_LOGIN_GUIDE_ITA_COUNT=1; THEME_STAY_TIME=299846; IS_HIDE_THEME_CHANGE=1; n_mh=2827XK1W1KqRZI7frLQwFG3nQeysug7zgymjuc_DuvE; sso_uid_tt=8962d3c99152241cee80d2e3d1037200; sso_uid_tt_ss=8962d3c99152241cee80d2e3d1037200; toutiao_sso_user=d6f2a461d52e8813bbf75ebf340c3d33; toutiao_sso_user_ss=d6f2a461d52e8813bbf75ebf340c3d33; sid_ucp_sso_v1=1.0.0-KGNkMjM5YjQxOGI2OTg0ZWU1MTRiYmUwMjIwMDY4ODZlMDczOGE5NDkKHQj5-8SP9wIQ6a3okwYY7zEgDDDb2rjZBTgGQPQHGgJsZiIgZDZmMmE0NjFkNTJlODgxM2JiZjc1ZWJmMzQwYzNkMzM; ssid_ucp_sso_v1=1.0.0-KGNkMjM5YjQxOGI2OTg0ZWU1MTRiYmUwMjIwMDY4ODZlMDczOGE5NDkKHQj5-8SP9wIQ6a3okwYY7zEgDDDb2rjZBTgGQPQHGgJsZiIgZDZmMmE0NjFkNTJlODgxM2JiZjc1ZWJmMzQwYzNkMzM; odin_tt=15528f44eb1323eb51e5d3d371a9205a74d9ab414cdc0ff3883e4f5f6c44c89af0566f1d1bf2efa041d96eb42cdf318db9307860bc3e604224cfcc9de058c549; sid_guard=d6f2a461d52e8813bbf75ebf340c3d33%7C1652168426%7C5184000%7CSat%2C+09-Jul-2022+07%3A40%3A26+GMT; uid_tt=8962d3c99152241cee80d2e3d1037200; uid_tt_ss=8962d3c99152241cee80d2e3d1037200; sid_tt=d6f2a461d52e8813bbf75ebf340c3d33; sessionid=d6f2a461d52e8813bbf75ebf340c3d33; sessionid_ss=d6f2a461d52e8813bbf75ebf340c3d33; sid_ucp_v1=1.0.0-KDIzMTBmZDZlZDY0ODY0YmE0MDc3MTdmZmRlYzMxYjkwOTFhNjFlMTYKHQj5-8SP9wIQ6q3okwYY7zEgDDDb2rjZBTgGQPQHGgJsZiIgZDZmMmE0NjFkNTJlODgxM2JiZjc1ZWJmMzQwYzNkMzM; ssid_ucp_v1=1.0.0-KDIzMTBmZDZlZDY0ODY0YmE0MDc3MTdmZmRlYzMxYjkwOTFhNjFlMTYKHQj5-8SP9wIQ6q3okwYY7zEgDDDb2rjZBTgGQPQHGgJsZiIgZDZmMmE0NjFkNTJlODgxM2JiZjc1ZWJmMzQwYzNkMzM; pwa_guide_count=3; __ac_signature=_02B4Z6wo00f013WzBAAAAIDCi.94Mcax03N1kwCAAL8e5Ge50BpOrcdXeruVhl5p63NIMAgCE4hINb8T-1ph-Wu8HAbi-85Q7X4uYFD5Tdk0t0ZzYzN9AWFJCqdLYthD1YkI7k4N9OlXgZ8a44; douyin.com; strategyABtestKey=1652427840.544; FOLLOW_NUMBER_YELLOW_POINT_INFO=MS4wLjABAAAABqG4fpbbIx2LZm9AQryXSe-hVrX2CAyHCAlqZKZyafY%2F1652457600000%2F0%2F1652427841644%2F0; msToken=YkPdbYyU7F34ZR73g84I6-5rx_JMAnCYIS68op1pF_gWMeuKI89F1KNqfOt7-Xxm1opYMgSFKxoRGL7LGz5ICjaAfvU54qnHr-bxbtU3m8B5ZKz4UgCzGQ==; home_can_add_dy_2_desktop=1; tt_scid=3HWBLiENjVow-68uiKDikc-9gEFccRhoI.ae2KsGF.tTf9huL2PrjqpTKstWTnUya5e2; msToken=DU5RwgVBS-Yc7z8gSprRp5C5mUqmlysm0Ib51s7b4rL_vnQ71ek050sVAQN0ej37EfDLqFqcDOEtKGdOZ-Pu4mWeXynXB5GrOADkmLy71Uwp9zoED-PjMQ==',
        'referer': 'https://www.douyin.com/user/MS4wLjABAAAASwhiL0bRi1X_zs7UhAIO2udbD1F_XKrsJMOaukl1Io4'
    }
    return headers


def get_urllist(user_id, user_name):
    # video_url_file = open("./video_url/" + user_name, "w")
    urllist = []
    max_cursor = str(int(time.time())) + "000"
    lenth = 20
    print('正在获取视频列表')
    while lenth != 0:
        headers = get_headers()
        headers["referer"] = "https://www.douyin.com/user/" + user_id
        try:
            url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={user_id}&max_cursor={max_cursor}&locate_query=false&count=20'
            # print(url)
            response = requests.get(url=url, headers=headers)
            # print("response.text",response.text)
            result = json.loads(response.text)
            max_cursor = result["max_cursor"]
            dataList = result["aweme_list"]
            lenth = len(dataList)
            for data in dataList:
                video_url = data["video"]["download_addr"]["url_list"][0]
                # print(video_url)
                # video_url_file.write(video_url + "\n")
                urllist.append(video_url)
            time.sleep(0.1)
        except Exception as e:
            print(e)
            traceback.print_exc()
    print(f'{user_id}总计{len(urllist)}个视频')
    return urllist


def download_mp4(urllist, name,save_path):
    map = {
        "success": [],
        "error": [],
    }
    output_path = save_path
    for url in urllist:
        try:
            filename = url.split("/")[3]
            print(f"正在下载mp4: {filename}")
            video_data = requests.get(url).content
            with open(f"{output_path}/{filename}.mp4", "wb") as f:
                f.write(video_data)
            print(f"{filename}下载完成")
            map["success"].append({url:filename})
            time.sleep(0.1)
        except Exception as e:
            print(e)
            print(f'{filename}下载失败')
            map["error"].append({url: filename})
    return map

def  main(args):
    save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
    os.makedirs(save_path,exist_ok=True)
    user_name = args["author"]
    user_id = args["url_list"][0].split("/")[-1].split("?")[0]
    urllist = get_urllist(user_id, user_name)
    return download_mp4(urllist, user_name,save_path)


if __name__ == "__main__":
    if not os.path.exists("./video_url/"):
        os.makedirs("./video_url/")
    input_path = sys.argv[1]
    for i in open(input_path, "r",encoding="utf-8"):
        user_name = i.strip().split(" ")[0]
        user_id = i.strip().split(" ")[1]
        get_urllist(user_id, user_name)
        urllist = []
        for l in open(f"./video_url/{user_name}", "r"):
            urllist.append(l.strip())

        download_mp4(urllist, user_name)
