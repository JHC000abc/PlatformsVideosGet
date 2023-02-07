# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@contact: JHC000abc@gmail.com
@file: bili_you_get_rewrite.py
@time: 2023/2/6 23:03 $
@desc:

"""
import os
import re
import json
from queue import Queue
from threading import Thread
from setting import setting


def process(args):
    save_path = os.path.join(setting.SAVE_PATH, args["platform"], args["kind"],args["language"], args["author"])
    os.makedirs(save_path,exist_ok=True)
    cmd = "you-get --playlist -o {} {}".format(save_path,args["url_list"][0])
    print("cmd=",cmd)
    os.system(cmd)


