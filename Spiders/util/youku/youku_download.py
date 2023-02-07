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
   'cookie': 'cna=PebaGq6qLHACAW/O1ht1MSTy; __ysuid=1651226976422us8; csrfToken=iVliHVUwKsEF6kG0Mx5UHub0; __ayft=1652702921512; __aysid=1652702921513hWi; __ayscnt=1; modalFrequency={"UUID":"10"}; xlly_s=1; redMarkRead=1; _m_h5_tk=ddf0b90ba02f173e8a159514361a2c0a_1652756861736; _m_h5_tk_enc=431839212b06e3a78a9e760baba17286; __arycid=dd-2-00; __arcms=dd-2-00; __ayvstp=47; __aysvstp=47; youku_history_word=%5B%22%25E7%2599%25BE%25E5%25AE%25B6%25E7%25A2%258E%25E6%2588%258F%22%2C%22%25E8%25A5%25BF%25E5%25AE%2589%25E8%2599%258E%25E5%25AE%25B6%22%5D; __arpvid=1652756860088thxqd8-1652756860118; __aypstp=25; __ayspstp=25; l=eBjvk41PLHeIj-k8BOfZlurza77TAIRAguPzaNbMiOCP_g5p9QKcW6fc3XT9CnGNh68yR3kS5jjYBeYBcncBW1IPhxa5kODmn; tfstk=cKVABOmNyaLvrIu88-Bu7k8zBPQlZvItVEiM65CM9SillqAOi1P39TVdhViEDaC..; isg=BFZW_EQDKKINKxzuSU-dZID1pwpY95oxhBc-GsC_aTnyg_YdKITyQBN9GxdvK5JJi',
   'referer': 'https://www.youku.com/profile/index/?spm=a2h0c.8166622.PhoneSokuPgc_1.dportrait&uid=UMzczNzA0NTQ2MA=='
   }
   return headers


def get_urllist(user_id,user_name):
    urllist = []
    # video_url_file = open(f"./video_url/{user_name}","w")
    length = 20
    page_num = 1
    print(f'正在获取视频列表')
    while length != 0:
        headers = get_headers()
        try:
            url = f'https://www.youku.com/profile/profile-data?type=video&pageNo={page_num}&nextSession=%7B%22subIndex%22%3A136%2C%22trackInfo%22%3A%7B%22parentdrawerid%22%3A%224433%22%7D%2C%22spmA%22%3A%22miniapp%22%2C%22spmC%22%3A%22drawer2%22%2C%22spmB%22%3A%22homepage%22%2C%22index%22%3A2%2C%22pageName%22%3A%22page_miniapp%22%2C%22scene%22%3A%22home_page_component_paging%22%2C%22scmB%22%3A%22rcmd%22%2C%22path%22%3A%22EP500689%22%2C%22scmA%22%3A%2220140689%22%2C%22scmC%22%3A%2224776%22%2C%22id%22%3A24776%7D&uid={user_id}&isGray=0&extend=%7B%7D&_=1652757123166'
            print(url)
            response =requests.get(url=url,headers=headers)
            result = json.loads(response.text)
            page_num += 1
            
            comList = result["data"]["componentList"]
            if len(comList)  == 0:
                break
            for component in comList:
                comId = component["componentId"]
                print(comId)
                if comId != "pc-profile-video":
                    continue
                dataList = component["moduleList"]
                lenth = len(dataList)
                for data in dataList:
                    video_url = data["data"]["videoLink"]
                    print(video_url)
                    urllist.append(video_url)
                    # video_url_file.write("https:"+video_url+"\n")
            time.sleep(0.1)
        except Exception as e:
            print(e)
            traceback.print_exc()
    print(f'{user_id}总计{len(urllist)}个视频')
    return urllist

def download_mp4(urllist,name,save_path):
    map = {
        "success": [],
        "error": [],
    }
    output_path = save_path
    for url in urllist:
        print("url",url)
        filename = url.split("/")[4].split("==")[0]
        try:
            print(f"正在下载视频: {filename}")
            cmd = f'you-get {"https:"+url} -o "{output_path}"'
            print(cmd)
            os.system(cmd)
            print(f"{filename}下载完成")
            map["success"].append({url, filename})
            time.sleep(0.1)
        except Exception as e:
            print(e)
            print(f'{filename}下载失败')
            map["error"].append({url, filename})
    return map

def flvToMp4(name,save_path):
    filelist = os.listdir(save_path)
    for filename in filelist:
        if filename.endswith(".flv"):
            try:
                flv_path = os.path.join(save_path,filename)
                mp4_path = flv_path.replace(".flv",".mp4")
                cmd = f"./ffmpeg -i {flv_path} -c copy {mp4_path}"
                print(cmd)
                print("flv转为mp4")
                os.system(cmd)
                os.remove(flv_path)
            except Exception as e:
                print(e)

def main(args):
    save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
    os.makedirs(save_path, exist_ok=True)
    user_name = args["author"]
    user_id = args["url_list"][0].split("/")[-1].split(".html")[0].replace("id_","")
    # user_id = "XMjk5ODI4MzQwOA=="
    # urllist = get_urllist(user_id, user_name)
    urllist = [i.replace("https:", "") for i in args["url_list"]]
    # urllist = args["url_list"]
    print(args["url_list"][0])
    print(user_id)
    print("urllist",urllist)
    if urllist:
        info = download_mp4(urllist, user_name,save_path)
        flvToMp4(user_name,save_path)
        return info
    else:
        return {"可下载视频数":0}





if __name__ == "__main__":
    if not os.path.exists("./video_url/"):
        os.makedirs("./video_url/")
    input_path = sys.argv[1]
    for i in open(input_path,"r",encoding="utf-8"):
        user_name = i.strip().split(" ")[0]
        user_id = i.strip().split(" ")[1]
        get_urllist(user_id,user_name)
        urllist = [] 
        for l in open(f"./video_url/{user_name}","r"):
            urllist.append(l.strip())
     
        download_mp4(urllist, user_name)
        flvToMp4(user_name)
