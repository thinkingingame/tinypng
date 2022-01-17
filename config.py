#!/usr/bin/python
# -*- coding: UTF-8 -*-

includeFileExt = [".png", ".jpg", ".webp"]      # 压缩文件类型（扩展名）
exludeFileDir = []    # 不要压缩的目录

# 任务执行结果
taskResult = {"Success": 0, "Skip": 1, "Fail": 2}

# 日志文件
logFile = "./log.txt"

# 压缩率底限，大于这个数就不去下载
compressRatio = 0.95

# 窗口属性
MAIN_WINDOW_TITLE = "SuperPng v0.1"
MAIN_WINDOW_SIZE = [800, 400]
DROP_FRAME_HEIGHT = 400