# !/usr/bin/env python3
import json
import traceback
import requests
import os
import time
from setting import setting

jiemu_list = ["粤韵风华","粤讲越掂","广东电影报道","光影视界","万家灯火","生活调查团","天眼追击"]

m3u8_list_path = os.path.join(setting.SAVE_PATH,"m3u8_list")
m3u8_path = os.path.join(setting.SAVE_PATH,"m3u8")
def get_m3u8_urllist():
    f = open("task_47232","rb")
    count = 0
    while True:
        line = f.readline()
        count += 1
        print(count)
        if not line:
            break
        else:
            try:
                line_str = str(line,encoding="utf-8")
                web_url = line_str.strip().split("\t")[0]
                jsonStr = line_str.strip().split("\t")[-1]
                info = json.loads(jsonStr)
                print(info)
                
                url = info["video_url"]["url"]
                title = info["video_url"]["title"]
                if title in jiemu_list:
                     w = open(m3u8_list_path+title,"a+")
                     m3u8_url = url.replace("\"","")+".m3u8\n"
                     if m3u8_url.startswith("http"):
                         w.write(m3u8_url)
            except:
                traceback.print_exc()

def get_data(url,retry=3):
    flag=False
    video_data = ""
    while not flag and retry>0:
        try:
            video_data = requests.get(url)
            flag=True
        except:
            retry-=1
    return video_data


def get_m3u8_file(save_path):
    try:
        for jiemu in jiemu_list:
            print(jiemu)
            for i in open(m3u8_list_path+jiemu,"r"):
                
                m3u8_url = i.strip().replace("v2-grtn.itouchtv.cn","vod.gdtv.cn")
                if m3u8_url.split("/")[-2] == "tv":
                    continue
                filename = m3u8_url.split("/")[-1]
                output_path = os.path.join(m3u8_path,jiemu)+ "/"
                # filepath = save_path
                filepath = f"{output_path}{filename}"
                print(f"正在下载m3u8文件 {m3u8_url}")
                # file_data = requests.get(m3u8_url).content
                file_data = get_data(m3u8_url)
                if file_data != "":
                    file_data = file_data.content
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    if os.path.exists(filepath):
                        continue
                    with open(f"{filepath}",mode="wb") as f:
                        f.write(file_data)
                    time.sleep(2)
    except Exception as e:
        print(e)



def get_mp4_file(m3u8_list_path,jiemu,save_path):
    map = {
        "success": [],
        "error": [],
    }
    m3u8_list = os.listdir(os.path.join(m3u8_path,jiemu))
    output_path = os.path.join(save_path,jiemu)
    for m3u8_filename in m3u8_list:
        m3u8_filepath = f"{output_path}{m3u8_filename}.ts"
        ts_file = os.path.join(m3u8_path, jiemu, m3u8_filename)
        try:
            count = 0
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            if os.path.exists(m3u8_filepath):
                os.remove(m3u8_filepath)
            mp4_filepath = m3u8_filepath.replace(".ts",".mp4")
            if os.path.exists(mp4_filepath):
                continue

            for i in open(ts_file,"r"):
                line = i.strip()
                if line.startswith("#"):
                    continue
                if line.startswith("http"):
                    count += 1
                    print(f"正在下载ts文件 {line}")
                    # file_data = requests.get(line).content
                    file_data = get_data(line)
                    if file_data != "":
                        file_data = file_data.content
                        with open(m3u8_filepath,mode="ab") as f:
                            f.write(file_data)
            cmd = f'./ffmpeg -i {m3u8_filepath} -c copy -map 0:v -map 0:a {mp4_filepath}'
            os.system(cmd)
            map["success"].append({jiemu: ts_file})
        except Exception as e:
            print(e)
            map["error"].append({jiemu: ts_file})
        if os.path.isfile(m3u8_filepath):
            os.remove(m3u8_filepath)
    return map


def main(args):
    save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
    os.makedirs(save_path, exist_ok=True)
    get_m3u8_file(save_path)
    res_map = {}
    for jiemu in jiemu_list:
        res_map[jiemu] = get_mp4_file(m3u8_list_path,jiemu,save_path)
    return res_map

if __name__ == "__main__":
    #get_m3u8_urllist()
    get_m3u8_file() 
    for jiemu in jiemu_list:
        get_mp4_file(m3u8_list_path,jiemu)  
