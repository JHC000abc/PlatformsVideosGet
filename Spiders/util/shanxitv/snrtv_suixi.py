from lxml import etree

import requests as req
import os
import requests
from setting import setting

class SendHttpRequests():
    def __init__(self):
        self.list_page_urls = [
            '''http://www.snrtv.com/snr_suixi/index.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
            '''http://www.snrtv.com/snr_suixi/index_2.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
            '''http://www.snrtv.com/snr_suixi/index_3.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
            '''http://www.snrtv.com/snr_suixi/index_4.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
            '''http://www.snrtv.com/snr_suixi/index_5.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
            '''http://www.snrtv.com/snr_suixi/index_6.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
            '''http://www.snrtv.com/snr_suixi/index_7.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
            '''http://www.snrtv.com/snr_suixi/index_8.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
            '''http://www.snrtv.com/snr_suixi/index_9.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
            '''http://www.snrtv.com/snr_suixi/index_10.html''',  # 碎戏 - 陕西网络广播电视台-陕西最大音视频新闻门户 www.snrtv.com
        ]
        self.info_page_urls = []
        self.video_urls = []

    def get_info_page_url(self):
        for list_page_url in self.list_page_urls:
            resp = self.get_data(list_page_url).content.decode()
            data = etree.HTML(resp)
            info_page_urls = data.xpath('''//div[@class="pic"]/a/@href''')
            for url in info_page_urls:
                self.info_page_urls.append(url)

    def get_vidio_url(self):
        self.get_info_page_url()
        for url in self.info_page_urls:
            data = etree.HTML(self.get_data(url).content.decode())
            v_src = data.xpath('''//p[@class="videoBox"]/@data-src''')
            print(v_src[0])
            self.video_urls.append(v_src[0])

    def parse(self):
        self.get_vidio_url()
        return self.video_urls


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
                filename = url.split("/")[-1]
                print(f"正在下载mp4: {filename}")
                # video_data = requests.get(url).content
                video_data = self.get_data(url)
                with open(f"{output_path}{filename}","wb") as f:
                    f.write(video_data)
                print(f"{filename}下载完成")
                map["success"].append({url: filename})
            except Exception as e:
                print(e)
                print(f'{filename}下载失败')
                map["error"].append({url: filename})
        return map

    def main(self,args):
        save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
        os.makedirs(save_path, exist_ok=True)
        video_urls = self.parse()
        return self.download_mp4(video_urls, args["author"],save_path)



if __name__ == "__main__":
    SendHttpRequests = SendHttpRequests()
    print(f"正在获取视频地址")
    video_urls = SendHttpRequests.parse()
    SendHttpRequests.download_mp4(video_urls,"百家碎戏")
         
    
