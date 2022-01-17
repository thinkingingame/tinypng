import time
import os

from config import *
from event import *

def writeLog(log):
    strLog = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "] " + log["content"]
    print(strLog)
    if log["isSendToUI"] == True:
        event.emit("SHOW_LOG", log["content"])
        # pass
    with open(logFile, mode="a+") as file:
        file.write(strLog + "\n")

if __name__ == "__main__":
    pass