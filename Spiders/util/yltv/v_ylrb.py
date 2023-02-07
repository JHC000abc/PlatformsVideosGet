import json
import os
import re

import requests as req
from lxml import etree
from setting import setting


class Ylrb():
    def __init__(self):
        self.start_urls = [
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/1''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/2''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/3''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/4''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/5''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/6''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/7''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/8''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/9''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/10''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/11''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/12''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/13''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/14''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/15''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
            '''http://v.ylrb.com/index.php?r=video/show/cid/28/page/16''',
            # 百姓剧场视频列表 - 榆林视听-榆林传媒中心（榆林日报、榆林广播电视台）新媒体-榆林地方视频门户站[YLWLTV.COM] - Powered By 威视
        ]
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
        self.info_urls = []
        self.m3u8_urls = []
        self.url_date = {}

    def start_requests(self):
        '''
        获取到页面含有 m3u8 链接内容的链接, 视频的名称;
        :return: 含有 m3u8 内容的链接 list, url 和 视频名称 的 dict;
        '''
        while 1:
            if not self.start_urls:
                break
            start_url = self.start_urls.pop()
            data = etree.HTML(self.get_data(start_url).text)
            info_urls = data.xpath(
                '''//div[contains(@class, 'pl2')]//a[contains(@class, 'pic')]/@href'''
            )
            date_list = data.xpath(
                '''//div[contains(@class, 'pl2')]//dd[contains(text(), '发布')]//text()'''
            )
            for info_url, date in zip(info_urls, date_list):
                self.url_date[info_url] = date.replace('发布', '').replace('：', '')
                self.info_urls.append(info_url)

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

    def parse(self,args):
        map = {
            "success": [],
            "error": [],
        }
        save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
        os.makedirs(save_path,exist_ok=True)
        self.start_requests()
        for info_url in self.info_urls:
            resp = self.get_data(info_url).content.decode()
            # 最后合成 mp4 文件的名字
            mp4Name = re.search(
                '<meta\s{0,3}name=\"Keywords\"\s{0,3}content=\"(.*?)\"\s{0,5}/>',
                resp, re.S
            ).group(1).replace('\t', '').replace(' ', '')
            #os.system('mkdir data/{}'.format(mp4Name))
            #print(f'已创建目录------{mp4Name}')
            # 正则表达式匹配时间字符串, 后面拼接请求用
            try:
                dateString = re.findall('var imgUrl = "http://.*?/(\d+-\d+-\d+)/.*?jpg\";', resp, re.S)[0]
            except:
                dateString = self.url_date.get(info_url, '')
            # 后面两个字段儿从这一段儿正则表达式里面去进行匹配
            mainString = re.findall(
                'div id=\"swfplayer\"><script src=\"(.*?)\" type=\"text/javascript\"></script>',
                resp)[0]
            vidString = re.search('vid=(.*?)&', mainString).group(1)
            siteidString = re.search('siteid=(.*?)&', mainString).group(1)
            # 构造请求
            get_m3u8_url = f'https://p.bokecc.com/servlet/getvideofile?vid={vidString}&siteid={siteidString}&width=980&useragent=other&hlssupport=1&vc&mediatype=1'
            # 处理 json
            resp = json.loads(self.get_data(get_m3u8_url).content.decode().replace('null(', '').replace(')', ''))
            # m3u8Url = resp.get('copies', '')[0].get('backupurl', '').replace('http', 'https')
            m3u8Url = resp.get('copies', '')[0].get('playurl', '').replace('http', 'https')
            # 获取到域名前面的字符串儿, 后面发送请求做拼接使用
            urlPartString = re.search('://(cm\d+-c\d+-\d+)\.play', m3u8Url).group(1)
            # 发送 m3u8 的请求 解析响应
            lines = self.get_data(m3u8Url).text.split('\n')
            # 逐行解析发送请求获取响应
            try:
                for line in lines:
                    if '#EXT' not in line or '' == line:
                        # 拼接 构造 .ts 文件的请求
                        try:
                            stringPartTxt = re.search('([A-Z0-9-]+\.ts)', line).group(1)
                        except:
                            continue
                        flagVideoStrPart = re.search('video=(\d+)', line).group(1)
                        if len(flagVideoStrPart) == 1:
                            flagVideoStr = '00{}'.format(flagVideoStrPart)
                        elif len(flagVideoStrPart) == 2:
                            flagVideoStr = '0{}'.format(flagVideoStrPart)
                        else:
                            flagVideoStr = flagVideoStrPart
                        downloadTsUrl = f'https://{urlPartString}.play.bokecc.com/flvs/{siteidString}/{dateString}/{line}'
                        tx_save_file = os.path.join(save_path, f'{mp4Name}.ts')
                        ts_text = open(tx_save_file, 'ab')
                        resp = self.get_data(downloadTsUrl).content
                        ts_text.write(resp)
                        print(f'文件---{ts_text}---已下载')

                print(f'名为---{mp4Name}---的所有 .ts 文件已下载完成')
                map["success"].append({lines: tx_save_file})
                # 合成 mp4 文件
                # os.system(f'cat output/{mp4Name}/*.ts > data/{mp4Name}/{mp4Name}.ts')
                os.system(f'./ffmpeg -i output/{mp4Name}.ts -c copy -map 0:v -map 0:a output/{mp4Name}.mp4')
                os.remove(f'./output/{mp4Name}.ts')
                # os.system(f'mv data/{mp4Name}/{mp4Name}.mp4 data/{mp4Name}.mp4')
                # os.system(f'rm -rf data/{mp4Name}')
            except Exception as e:
                print(e,e.__traceback__.tb_lineno)
                map["error"].append({lines})
            return map




# if __name__ == '__main__':
#     os.system('mkdir output')
#     Ylrb = Ylrb()
#     Ylrb.parse()
