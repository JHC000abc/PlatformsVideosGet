# !/usr/bin/env python3
import re
import os
import requests as req
from lxml import etree
from setting import setting

class TvBaoji():
    def __init__(self):
        self.start_urls = [
            '''http://www.tvbaoji.com/public/nongyesiji.shtml''',  # 宝鸡网络电视台 宝鸡电视台 宝鸡资讯网
            '''http://www.tvbaoji.com/public/nongyesiji_2.shtml''',  # 宝鸡网络电视台 宝鸡电视台 宝鸡资讯网
            '''http://www.tvbaoji.com/public/nongyesiji_3.shtml''',  # 宝鸡网络电视台 宝鸡电视台 宝鸡资讯网
            '''http://www.tvbaoji.com/public/nongyesiji_4.shtml''',  # 宝鸡网络电视台 宝鸡电视台 宝鸡资讯网
            '''http://www.tvbaoji.com/public/nongyesiji_5.shtml''',  # 宝鸡网络电视台 宝鸡电视台 宝鸡资讯网
            '''http://www.tvbaoji.com/public/nongyesiji_6.shtml''',  # 宝鸡网络电视台 宝鸡电视台 宝鸡资讯网
        ]
        self.list_page_urls = []
        self.download_urls = []

    def get_list_page_urls(self):
        while 1:
            if not len(self.start_urls):
                break
            start_url = self.start_urls.pop()
            data = etree.HTML(req.get(start_url).text)
            list_page_url_part_list = data.xpath('''//div[@class="content clearfix"]//li/a/@href''')
            for list_page_url_part in list_page_url_part_list:
                list_page_url = 'http://www.tvbaoji.com/' + list_page_url_part
                self.list_page_urls.append(list_page_url)

    def parse(self):
        self.get_list_page_urls()
        for list_page_url in self.list_page_urls:
            src_num = re.search('cms(\d+)article', list_page_url).group(1)
            redirect_url = f'http://www.tvbaoji.com/soms4/web/jwzt/player/PlayerJS.jsp?channelId=-1&fileId=7354&width=880px&height=495px&newsId={src_num}'
            # resp = req.get(redirect_url).text
            resp = self.get_data(redirect_url).text
            download_url = re.search('''innerHTML=\"<video  src=\'(.*?)\'''', resp).group(1)
            self.download_urls.append(download_url)
            # print(download_url)
        return self.download_urls

    def download_mp4(self,urllist,name,save_path):
        map = {
            "success": [],
            "error": [],
        }
        output_path = save_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        for url in urllist:
            try:
                filename = url.split("@")[-1]
                print(f"正在下载mp4: {filename}")
                # video_data = req.get(url).content
                video_data = self.get_data(url)
                if video_data != "":
                    print(f"{output_path}/{filename}.mp4")
                    with open(f"{output_path}/{filename}.mp4", "wb") as f:
                        f.write(video_data)
                    print(f"{filename}下载完成")
                    map["success"].append({url: filename})
                else:
                    print("请求异常")
            except Exception as e:
                print(e)
                print(f'{filename}下载失败')
                map["error"].append({url: filename})


        return map

    def get_data(self,url,retry=3):
        flag=False
        video_data = ""
        while not flag and retry>0:
            try:
                video_data = req.get(url)
                flag=True
            except:
                retry-=1
        return video_data

    def main(self,args):
        save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
        os.makedirs(save_path, exist_ok=True)
        video_urls = self.parse()
        print("video_urls",video_urls)
        return self.download_mp4(video_urls, args["author"],save_path)

if __name__ == '__main__':
    TvBaoji = TvBaoji()
    video_urls = TvBaoji.parse()
    TvBaoji.download_mp4(video_urls, "乡村行")
