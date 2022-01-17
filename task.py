#!/usr/bin/python
# -*- coding: UTF-8 -*-

from multiprocessing import Pool, Manager, active_children
import threading

from config import *
from tinypng import *
from log import *
from logutils import *

totalCount = 0          # 总的图片数量
successCount = 0        # 成功压缩数量
skipDownloadCount = 0   # 跳过下载数量，如果压缩率大于0.95就不下载了，用原来的
failCount = 0           # 失败个数

# 失败的文件重试次数
failRetryCount = 0

globalResultQueue = None
globalLogQueue = None

pool = None
isStopMasterForce = False

# 异步执行任务
def startOneTaskAsync(file):
    global globalResultQueue
    global globalLogQueue
    globalLogQueue.put_nowait(packLogSendUI("start task:" + file))
    response = uploadFile(file, globalLogQueue)
    if response == None:
        globalLogQueue.put_nowait(packLogSendUI("response is None"))
        globalLogQueue.put_nowait(packLogSendUI("error file:" + file))
        globalResultQueue.put_nowait({file: taskResult["Fail"]})
    if "error" in response.keys():
        globalLogQueue.put_nowait(packLogSendUI(response["error"]))
        globalLogQueue.put_nowait(packLogSendUI("error file:" + file))
        globalResultQueue.put_nowait({file: taskResult["Fail"]})
    else:
        ratio = response["output"]["ratio"]
        if ratio <= compressRatio:   # 压缩较少，舍弃
            result = downloadFile(response["output"]["url"], file, globalLogQueue)
            if result:
                globalLogQueue.put_nowait(packLogSendUI("success task:" + file))
                globalResultQueue.put_nowait({file: taskResult["Success"]})
            else:
                globalLogQueue.put_nowait(packLogSendUI("download fail"))
                globalLogQueue.put_nowait(packLogSendUI("error file:" + file))
                globalResultQueue.put_nowait({file: taskResult["Fail"]})
        else:
            globalLogQueue.put_nowait(packLogSendUI("skip download:" + file))
            globalResultQueue.put_nowait({file: taskResult["Skip"]})

def initPool(resultQueue, logQueue):
    global globalResultQueue
    globalResultQueue = resultQueue
    global globalLogQueue
    globalLogQueue = logQueue

# 停止所有任务
def stopAllTask():
    global pool
    global isStopMasterForce
    isStopMasterForce = True
    if pool != None:
        pool.terminate()
        pool = None

# 创建一个任务主线程
def startMasterThread(compressFiles):
    resultQueue = Manager().Queue()
    logQueue = Manager().Queue()
    results = {}
    global pool
    global isStopMasterForce
    pool = Pool(processes=16, initializer=initPool, initargs=[resultQueue, logQueue])
    for file in compressFiles:
        if pool._state == "RUN":
            pool.apply_async(startOneTaskAsync, args=[file])
    pool.close()
    # pool.join()
    while True:
        if isStopMasterForce:
            break
        if not logQueue.empty():
            for i in range(logQueue.qsize()):
                writeLog(logQueue.get_nowait())
        if not resultQueue.empty():
            for i in range(resultQueue.qsize()):
                result = resultQueue.get_nowait()
                for file in result:
                    results[file] = result[file]
        childrenCount = len(active_children())
        if childrenCount <= 0 or len(results) >= len(compressFiles):
            cleanQueue([resultQueue, logQueue])
            handleResult(results, compressFiles)
            break

# 清空队列
def cleanQueue(queues):
    for q in queues:
        while not q.empty():
            try:
                for i in range(q.qsize()):
                    q.get(timeout=0.001)
            except:
                pass

# 异步执行任务
def startAsync(compressFiles, isReset = True):
    if isReset:
        reset()
    master = threading.Thread(target=startMasterThread, name='MasterThread', args=[compressFiles])
    master.start()

def reset():
    global isStopMasterForce
    global totalCount, successCount, skipDownloadCount, failCount, failRetryCount
    totalCount = 0
    successCount = 0
    skipDownloadCount = 0
    failCount = 0
    failRetryCount = 0
    isStopMasterForce = False

 # 处理结果
def handleResult(resultDict, compressFiles):
    global totalCount, successCount, skipDownloadCount, failCount, failRetryCount
    if totalCount == 0:
        totalCount = len(compressFiles)
    failCount = 0
    failTask = []
    for file in resultDict.keys():
        result = resultDict[file]
        if result == taskResult["Success"]:
            successCount = successCount + 1
        elif result == taskResult["Skip"]:
            skipDownloadCount = skipDownloadCount + 1
        elif result == taskResult["Fail"]:
            failCount = failCount + 1
            failTask.append(file)
    
    if len(failTask) > 0:
        if failRetryCount < 3:
            failRetryCount = failRetryCount + 1
            writeLog(packLogSendUI("retry count:" + str(len(failTask))))
            startAsync(failTask, isReset = False)
        else:
            onAllTaskFinished(failTask)
    else:
        onAllTaskFinished(failTask)

def onAllTaskFinished(failTask):
    printResult(failTask)
    event.emit("ALL_TASK_FINISHED")

def printResult(files):
    global totalCount, successCount, skipDownloadCount, failCount, failRetryCount
    writeLog(packLogSendUI("==============================================================="))
    writeLog(packLogSendUI("total count:{}, success count:{}, skip count:{}, fail count:{}".format(str(totalCount), str(successCount), str(skipDownloadCount), str(failCount))))
    writeLog(packLogSendUI("==============================================================="))
    if len(files) > 0:
        writeLog(packLogSendUI("fail files:"))
        for file in files:
            writeLog(packLogSendUI(file))
        writeLog(packLogSendUI("==============================================================="))



if __name__ == "__main__":
    startAsync(["aaaa"])