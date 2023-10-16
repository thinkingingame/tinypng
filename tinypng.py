#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import ssl
import requests
import time
import yaml
import traceback
import random

from logutils import *

# 随机IP地址
def getRandomIP():
    ip = []
    for i in range(4):
        ip.append(str(random.randint(0, 255)))
    return '.'.join(ip)

# 上传图片
def uploadFile(file, logQueue):
    url = "https://tinypng.com/backend/opt/shrink"
    headers = {
        'X-Forwarded-For' : getRandomIP(),
        "Content-Type": "multipart/form-data",
        "rejectUnauthorized": "false",
        'Postman-Token': str(time.time()),
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    with open(file, mode="rb")as f:
        response = None
        try:
            response = requests.post(url=url,data=f.read(),headers=headers,timeout=10)
            response.close()
        except Exception as e:
            response = None
            logQueue.put_nowait(packLogNotSendUI(traceback.format_exc()))

        if response != None and response.status_code == 201:
            try:
                return yaml.safe_load(response.content)
            except Exception as e:
                logQueue.put_nowait(packLogNotSendUI(response.content))
                logQueue.put_nowait(packLogNotSendUI(traceback.format_exc()))
                return None

# 写文件
def writeToFile(response, filePath, logQueue):
    dir = os.path.dirname(filePath)
    if not os.path.exists(dir):
        os.makedirs(dir)
    try:
        with open(filePath, mode="wb")as f:
            f.write(response.content)
            return True
    except:
        logQueue.put_nowait(packLogNotSendUI("write to file error"))
        return False

# 下载文件
def downloadFile(url, downloadDir, logQueue):
    response = None
    try:
        response = requests.get(url,timeout=10)
        response.close()
    except:
        logQueue.put_nowait(packLogNotSendUI(traceback.format_exc()))
    if response != None and response.status_code == 200:
        return writeToFile(response, downloadDir, logQueue)
    return False