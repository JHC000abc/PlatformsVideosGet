"""you-get 下载"""
import sys
import os


def download_video(out_dir, url):
    """
       download_video
       args: out_dir, url
    """
    filename = url.split("/")[-1]
    out_path = os.path.join(out_dir,filename)
    cmd = "you-get " + url + " -O " + out_path
    print(cmd)
    os.system(cmd)    

if __name__ == "__main__":
    file_path = sys.argv[1]
    out_dir = sys.argv[2]
    for i in open(file_path,"r",encoding="utf-8"):
        i = i.strip()
        up_name = i.split("\t")[0]
        url = i.split("\t")[1]
        output_dir = os.path.join(out_dir, up_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        download_video(output_dir, url)
