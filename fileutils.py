#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import os

from config import *

# 过滤不用压缩的文件
def filterImageFile(file):
    for ext in includeFileExt:
        if file.endswith(ext):
            return True
    return False

def filterDir(file):
    for dir in exludeFileDir:
        result = re.search(dir, file)
        if result != None:
            return False
    return True

# 遍历目录，进行压缩
def findImageFile(rootPath):
    result = []
    dirs = []
    # 处理多个文件和目录
    def splitPath():
        paths = rootPath.split(" ")
        for path in paths:
            if os.path.isfile(path):
                if filterImageFile(path):
                    result.append(path)
            elif os.path.isdir(path):
                dirs.append(path)

    def listFile(srcPath):
        files = os.listdir(srcPath)
        for file in files:
            fileAbsPath = os.path.join(srcPath, file)
            if os.path.isdir(fileAbsPath):
                listFile(fileAbsPath)
            else:
                if filterImageFile(fileAbsPath) and filterDir(fileAbsPath):
                    result.append(fileAbsPath)
    splitPath()
    for dir in dirs:
        listFile(dir)
    return result

if __name__ == "__main__":
    print(findImageFile("D:/work/project/dev/script/xupdate"))