import requests
import json
import os
import re
import time
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from setting import setting


def get_urllist(user_id):
    length = 30
    urllist = []
    page = 0
    while length != 0:

        headers = {
            "authority": "www.ixigua.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "dnt": "1",
            "referer": "https://www.ixigua.com/home/48024653936231/?source=pgc_author_name&list_entrance=anyVideo",
            "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "x-secsdk-csrf-token": "0001000000014dea0527b61a384490421e9bfbba8f47f670d7e5ce1b73f8a9ebb01d9ca499d417414660ab0b6166"
        }


        params = {
             "to_user_id": "{}".format(user_id),
             "offset": "{}".format(page*30),
             "limit": "30",
             "maxBehotTime": "1587264639",
             "order": "new",
             "isHome": "0",
             "msToken": "hZxJx4EKm1t5UqJ6AjkQjUTCFwTlFo7ooUQc71eEFLqFbmwro20JTHVNfTv2sop_b0IXariBZJF0ckGFjo8OWijp_XPCGS5IDAK8cdMlsvYNY8Vy6clZ",
             "X-Bogus": "DFSzswVYGNkANaVHSh1-cM9WX7rU",
             "_signature": "_02B4Z6wo00001aMdHMAAAIDBIx.mgTp3ns2jHRhAAAsnBLDeLAWBDwN1ETm79ubL3dEfDHfLCvXZkOO2Qhw3c4fZtA.WkJXEe9VYjz2mGNYlOhykTCUXteweXQeXwdIS4q3nXVRvHoblh4A3e8"
        }
        url = "https://www.ixigua.com/api/videov2/author/new_video_list"
        try:
            # print("url:  " + url)
            response = requests.get(url=url, headers=headers,params=params)
            result = json.loads(response.text)
            # print("result",result)
            dataList = result["data"]["videoList"]
            length = len(dataList)
            if length == 1:
                break
            page += 1
            for data in dataList:
                if "group_id" in data:
                    video_url = "https://www.ixigua.com/embed?group_id="+data["group_id"]
                    # print(video_url)
                    urllist.append(video_url)
            # print(length)
            time.sleep(1)
        except Exception as e:
            print(e)
            traceback.print_exc()
         
    print(f'该博主爬取视频总数为{len(urllist)}')    
    return urllist

def get_mp4_url(url):
    #s = Service("./chromedriver")
    driver = webdriver.Chrome("./chromedriver")
    mp4_url = ""
    try:
        driver.get(url)
        driver.implicitly_wait(5)
        mp4_url = driver.find_element_by_xpath("//video[@mediatype='video']").get_attribute("src")
        print("mp4_url",mp4_url)
    except Exception as e:
        print(e)
        print(f'获取视频地址失败') 

    return mp4_url
         
def downloadMp4(url,user_name,save_path):
    map = {
        "success": [],
        "error": [],
    }
    filename = url.split("/")[3]
    print(f'正在下载{filename}')
    try:
        video_data =requests.get(url).content
                    
        output_path = save_path
 
        file_path = f"{output_path}{filename}.mp4"
 
        with open(file_path, mode="wb") as f:
            f.write(video_data)
        print(f"视频{filename}下载完成")
        map["success"].append({url: filename})
    except Exception as e:
        print(f"视频{filename}下载失败")
        map["error"].append({url: filename})

    return map

def main(args):
    save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
    os.makedirs(save_path, exist_ok=True)
    user_name = args["author"]
    url = args["url_list"][0]
    user_dict = {}
    if "home" in url and args["kind"]=="频道":
        user_id = url.split("home/")[-1].split("?")[0]
        user_dict[user_name] = user_id
        for k, v in user_dict.items():
            urllist = get_urllist(user_id)
            for i in urllist:
                mp4_url = get_mp4_url(i)
                if mp4_url != "":
                    return downloadMp4(mp4_url, k, save_path)

    elif args["kind"]=="短视频":
        # 短视频
        mp4_url = get_mp4_url(url)
        if mp4_url != "":
            return downloadMp4(mp4_url, user_name, save_path)
    else:
        pass







if __name__ == "__main__":
    a = os.listdir("./video_url/")
    user_dict = {}
    input_path = sys.argv[1]
    if not os.path.exists("./video_url/"):
        os.makedirs("./video_url/")
    for i in open(input_path,"r",encoding="utf-8"):
        line = i.strip()
        user_name = line.split("\t")[0]
        user_id = line.split("\t")[1]
        user_dict[user_name] = user_id
        print("user_dict",user_dict)
    for k,v in user_dict.items():
        if k in a:
            continue
        urllist = get_urllist(v)
        video_url_file = open(f"./video_url/{k}.txt",'w')
        for url in urllist:
            video_url_file.write(url+"\n")
        video_url_file.close()
    print(f'视频地址全部写入完成')
    for k,v in user_dict.items():
        print("k,v",k,v)
        for i in open(f"video_url/{k}.txt","r",encoding="utf-8"):
            print("i",i)
            url = i.strip()
            print("url = ",url)
            mp4_url = get_mp4_url(url)
            if mp4_url != "":
                downloadMp4(mp4_url, k) 
