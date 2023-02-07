# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@contact: JHC000abc@gmail.com
@file: setting.py
@time: 2023/2/6 20:31 $
@desc:

"""
import os
import re
import json
from queue import Queue
from threading import Thread



RUN_QUEUE = Queue()
SAVE_PATH = R"E:\JHC\spider"