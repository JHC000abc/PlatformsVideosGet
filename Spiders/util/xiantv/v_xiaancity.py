from lxml import etree
import requests
import os
from setting import setting


class VxianCity():
    def __init__(self):
        self.start_url_list = [
            '''http://v.xiancity.cn/folder6/folder76/folder502/?_gscu_=50870374aeu2xg21&_gscs_=50870374825myg21%7Cpv%3A2''',  # 西安最方言_西安网络广播电视台
            '''http://v.xiancity.cn/folder6/folder76/folder502/index_2.html''',  # 西安最方言_西安网络广播电视台
            '''http://v.xiancity.cn/folder6/folder76/folder502/index_3.html''',  # 西安最方言_西安网络广播电视台
        ]
        self.m3u8_url_list = []

    def get_url(self,save_path):
        output_path = os.path.join(save_path,"m3u8")
        os.makedirs(output_path,exist_ok=True)

        for start_url in self.start_url_list:
            data = etree.HTML(requests.get(start_url).content.decode())
            info_urls = data.xpath('''//ul[@class="clearfix"]//p//@href''')
            for info_url in info_urls:
                try:
                    dataObj = etree.HTML(requests.get(info_url).content.decode())
                    url = dataObj.xpath('''//input[contains(@id, 'm3u8')]/@value''')
                    m3u8_url = url[0]
                    filename  = m3u8_url.split("/")[-1]
                    filepath = f"{output_path}{filename}"
                    print(f"正在下载m3u8文件{m3u8_url}")
                    file_data = requests.get(m3u8_url).content
                    with open(f"{filepath}",mode="wb") as f:
                        f.write(file_data)
                except Exception as e:
                    print(e)
                    continue
        return self.m3u8_url_list
   
    def get_mp4_file(self,save_path):
        map = {
            "success": [],
            "error": [],
        }
        m3u8_list = os.listdir(os.path.join(save_path,"m3u8"))
        for m3u8_filename in m3u8_list:
          output_path = save_path
          if not os.path.exists(output_path):
              os.makedirs(output_path)
          m3u8_filepath = f"{output_path}{m3u8_filename}.ts"
          if os.path.exists(m3u8_filepath):
              os.remove(m3u8_filepath)
          mp4_filepath = m3u8_filepath.replace(".ts", ".mp4")
          try:

              if os.path.exists(mp4_filepath):
                  continue
              for i in open(os.path.join(os.path.join(save_path,"m3u8"),f"{m3u8_filename}"),"r"):
                  line = i.strip()
                  if line.startswith("#"):
                      continue
                  if line.startswith("http"):
                      print(f"正在下载ts文件 {line}")
                      file_data = requests.get(line).content
                      with open(m3u8_filepath,mode="ab") as f:
                          f.write(file_data)
              map["success"].append({m3u8_filename: m3u8_filepath})
              cmd = f'./ffmpeg -i {m3u8_filepath} -c copy -map 0:v -map 0:a {mp4_filepath}'
              os.system(cmd)
              if os.path.isfile(m3u8_filepath):
                  os.remove(m3u8_filepath)
          except Exception as e:
              print(e)
              print(f"{m3u8_filename}下载失败")
              map["error"].append({m3u8_filename: m3u8_filepath})
        return map

    def main(self,args):
        save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
        os.makedirs(save_path, exist_ok=True)
        self.get_url(save_path)
        return self.get_mp4_file(save_path)



if __name__ == "__main__":
    VxianCity = VxianCity()
    VxianCity.get_url()
    VxianCity.get_mp4_file()

