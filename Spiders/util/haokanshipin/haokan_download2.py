# !/usr/bin/env python3
import requests
import re
from random import choice
import time
import json
import os
import traceback
import sys
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
        'User-Agent': user_agent,
        'cookie': 'BAIDUID=AE89DE687C2E253608CF268812998A8D:FG=1; UUAP_TRACE_TOKEN=1739311346a45bdccba4bc89711c8cd3; BIDUPSID=AE89DE687C2E253608CF268812998A8D; PSTM=1649670184; UUAP_P_TOKEN=PT-723127153671938050-TKrf1vP6yv-uuap; SECURE_UUAP_P_TOKEN=PT-723127153671938050-TKrf1vP6yv-uuap; BSG_B_TOKEN=bArmkc9frRK6oLaSIzGTCRWnIc79GAw2TlVkz8FuFi8ps6NvyM0bCtoCV5c3aqrz9WhLwVRU6j5hi0d8WmYZ5w==; SECURE_BSG_B_TOKEN=bArmkc9frRK6oLaSIzGTCRWnIc79GAw2TlVkz8FuFi8ps6NvyM0bCtoCV5c3aqrz9WhLwVRU6j5hi0d8WmYZ5w==; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BAIDUID_BFESS=AE89DE687C2E253608CF268812998A8D:FG=1; BA_HECTOR=al01010kakagah8geh1h7k6aq0r; H_PS_PSSID=31254_36420_36165_34584_35979_36054_36433_36346_26350_36302_36313; PSINO=1; BCLID=10770947758514255106; BDSFRCVID=PbIOJexroG0xT95DfRH5u8KF17qMFyTTDYLEJs2qYShnrsPVJeC6EG0PtoWQkz--EHtdogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJ4J_IDKJK_3H48k-4QEbbQH-UnLqhvtX2OZ04n-ah02Dbc20fOqLncB5H7i0joLW23j2bom3UTKsq76Wh35K5tTQP6rLtbv3G54KKJxbPOiDqrGD-5tK4tQhUJiB5OLBan7Lj6IXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC_xj58aj6bXeU5eetjK2CntsJOOaCv-KqvOy4oWK441DMvBLpoR5m78V4KyWhLaDqvoKMnD3M04K4o9-hvT-54e2p3FBUQJoh5XQft20b0yWMcw-6Oa5jr2Qn7jWhk2Dq72ybDVQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCHJT0JtRFfoDv5b-0_qnjkbPjoKCCShUFX5-CsLe7A2hcHMPoosIJ1MlOGQ-Ld2HrtqUnltCjia-JvKfbUotoHMlQUMt4YQpo4-53p5ab4hl5TtUJMqUnzXR_2-4KX-p3yKMnitIj9-pnKHlQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuD60Mj5oBjNKs5JtXKD600PK8Kb7VbpDzjMnkbJkXhPtj2PTnLmn-5MPabCnvsCjzyUR2XPD7QbrH0xRfyNReQIO13hcdSR3yQqrpQT8r5hbv2x6ttIrhQJOMab3vOIJzXpO15CuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-Ftqj_s2I6yBbj8HJoHjJbGq4bohjPr-4r9BtQO-DOxoPnmfC5UexoSjJ_WyU5LjpQu0JcnQgnk2p5F-KoaofOdhR550hKpbt-q0x-jLTny-MjoMjCVsqnmb-nJyUnQhtnnBnKL3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CcJ-J8XMKtGe5rP; BCLID_BFESS=10770947758514255106; BDSFRCVID_BFESS=PbIOJexroG0xT95DfRH5u8KF17qMFyTTDYLEJs2qYShnrsPVJeC6EG0PtoWQkz--EHtdogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJ4J_IDKJK_3H48k-4QEbbQH-UnLqhvtX2OZ04n-ah02Dbc20fOqLncB5H7i0joLW23j2bom3UTKsq76Wh35K5tTQP6rLtbv3G54KKJxbPOiDqrGD-5tK4tQhUJiB5OLBan7Lj6IXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC_xj58aj6bXeU5eetjK2CntsJOOaCv-KqvOy4oWK441DMvBLpoR5m78V4KyWhLaDqvoKMnD3M04K4o9-hvT-54e2p3FBUQJoh5XQft20b0yWMcw-6Oa5jr2Qn7jWhk2Dq72ybDVQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCHJT0JtRFfoDv5b-0_qnjkbPjoKCCShUFX5-CsLe7A2hcHMPoosIJ1MlOGQ-Ld2HrtqUnltCjia-JvKfbUotoHMlQUMt4YQpo4-53p5ab4hl5TtUJMqUnzXR_2-4KX-p3yKMnitIj9-pnKHlQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuD60Mj5oBjNKs5JtXKD600PK8Kb7VbpDzjMnkbJkXhPtj2PTnLmn-5MPabCnvsCjzyUR2XPD7QbrH0xRfyNReQIO13hcdSR3yQqrpQT8r5hbv2x6ttIrhQJOMab3vOIJzXpO15CuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-Ftqj_s2I6yBbj8HJoHjJbGq4bohjPr-4r9BtQO-DOxoPnmfC5UexoSjJ_WyU5LjpQu0JcnQgnk2p5F-KoaofOdhR550hKpbt-q0x-jLTny-MjoMjCVsqnmb-nJyUnQhtnnBnKL3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CcJ-J8XMKtGe5rP; Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5=1652187079; ab_sr=1.0.1_ZGQyMzBmYzc2M2Y3NTJkMzAwMjA5YzI2YjVkYjZkYzUwZTJjYmYwMTgzMzVkYjBkYmQ3YmExYmRhNGIzMGUzNWQyYjc2MjUyNDIwZDQyMDBiOTg1YTNlOWFhYWJlZjMzM2ZkMjYyOWIyNmU3ZGM1NmRiNWIwZTcwYjNiMTBjZWM5YTdkMmM3ZjYyNGE0ZjVjOTU1N2NiNmYzNzNjNWY0OQ==; reptileData=%7B%22data%22%3A%22195ed18ffc90358fe2d348b2f8caf4f000b05fd2c18227ab0e4d04df1b5384ff3de2a1e7cfe7187b8a176ada04306f3b9f902082ebff49577b1954f27373d2e496eb53fb19f12033dbb45775e6e5b5a4f0104681303590a13d2df8f774b6778e%22%2C%22key_id%22%3A%2230%22%2C%22sign%22%3A%22b4866784%22%7D; hkpcSearch=%u4E8C%u72D7%u63A2%u5E97; Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5=1652187129; RT=\"z=1&dm=baidu.com&si=s4fxplpwr3&ss=l305j0b9&sl=4&tt=4m4&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf\"; ariaDefaultTheme=undefined'
    }
    return headers


def get_urllist(user_id):
    urllist = []
    try:
        ctime = str(int(time.time())) + "000000"
        has_more = 1
        while has_more == 1:
            headers = get_headers()
            headers[
                "cookie"] = 'BAIDUID=53ED023F7504FCEA2F8BDFAE0AFFAF24:FG=1; BSG_B_TOKEN=; SECURE_BSG_B_TOKEN=; av1_switch_v3=0; COMMON_LID=279cc2d224aaf133cbbd4512ae0a56d8; PC_TAB_LOG=video_details_page'
            url = f'https://haokan.baidu.com/web/author/listall?app_id={user_id}&ctime={ctime}&rn=10&searchAfter=&_api=1'
            print(url)
            response = requests.get(url=url, headers=headers)
            result = json.loads(response.text)
            has_more = result["data"]["has_more"]
            ctime = result["data"]["ctime"]
            dataList = result["data"]["results"]
            for data in dataList:
                video_url = "https://haokan.baidu.com/v?vid=" + data["content"]["vid"]
                urllist.append(video_url)
            time.sleep(2)
        print(f'{user_id}')
    except Exception as e:
        print(e)
        traceback.print_exc()
    return urllist


def get_mp4_urllist(urllist):
    mp4_urllist = []
    try:
        for url in urllist:
            headers = get_headers()
            print(url)
            response = requests.get(url=url, headers=headers)
            mp4_url = re.findall("\"previewUrlHttp\":\"(.*?)\",", response.text.encode("utf-8").decode("utf-8"))
            if len(mp4_url) != 0:
                mp4_urllist.append(mp4_url[0].replace("\\", ""))
            time.sleep(1)
    except Exception as e:
        print(e)
        traceback.print_exc()
    print(f"{len(mp4_urllist)}")
    return mp4_urllist


def download_mp4(urllist, name,save_path):
    map = {
        "success": [],
        "error": [],
    }
    output_path = save_path
    for url in urllist:
        filename = url.split("/")[6].split("?")[0]
        try:

        # if not os.path.exists(output_path):
        #     os.makedirs(output_path)

            print(url)
            print(f"downloading~~~ mp4: {filename}")
            video_data = requests.get(url).content
            with open(f"{output_path}/{filename}", "wb") as f:
                f.write(video_data)
            print(f"{filename} download success")
            time.sleep(2)
            map["success"].append({url: filename})
        except Exception as e:
            print(e)
            print(f'{filename} download faild')
            map["error"].append({url: filename})
    return map

def get_user_id(vid):
    url = "https://haokan.baidu.com/videoui/api/videoauthor"
    params = {
        "vid": vid
    }
    response = requests.get(url, params=params)
    response.encoding = "utf-8"

    mthid = json.loads(response.text)["data"]["response"]["author"]["mthid"]
    return mthid

def main(args):
    save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
    os.makedirs(save_path,exist_ok=True)
    user_name = args["author"]
    if args["kind"] =="短视频":

        vid = args["url_list"][0].split("?")[-1].replace("vid=","")
        user_id = get_user_id(vid)
        print("user_id",user_id,user_name)
        urllist = get_urllist(user_id)
        print("urllist",urllist)
        mp4_urllist = get_mp4_urllist(urllist)
        return download_mp4(mp4_urllist, user_name,save_path)
    elif args["kind"] =="频道":
        user_id = args["url_list"][0].split("/")[4].split("?")[0]
        urllist = get_urllist(user_id)
        print("urllist", urllist)
        mp4_urllist = get_mp4_urllist(urllist)
        return download_mp4(mp4_urllist, user_name, save_path)
    else:
        print(args["kind"],"没写逻辑")


if __name__ == "__main__":
    input_path = sys.argv[1]
    for i in open(input_path, "r"):
        user_name = i.strip().split(" ")[0]
        user_id = i.strip().split(" ")[1]

        urllist = get_urllist(user_id)
        mp4_urllist = get_mp4_urllist(urllist)
        download_mp4(mp4_urllist, user_name)