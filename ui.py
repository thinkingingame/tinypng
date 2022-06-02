#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import webbrowser

import tkinter as Tkinter
import tkinter.messagebox as MessageBox
from TkinterDnD2 import *

from config import *
from log import *
from logutils import *
from task import *
from fileutils import *

master = TkinterDnD.Tk()
textLog = None

isTaskInProgress = False
taskStartTime = 0

logQueue = []

def startCompress(rootPath):
    global isTaskInProgress
    global taskStartTime
    if isTaskInProgress:
        writeLog(packLogSendUI("Error:Performing other tasks..."))
        return
    isTaskInProgress = True
    taskStartTime = time.time()
    cleanLogText()
    paths = master.tk.splitlist(rootPath)
    writeLog(packLogSendUI("=================================input files=============================="))
    for path in paths:
        writeLog(packLogSendUI(str(path)))
    writeLog(packLogSendUI("=========================================================================="))
    files = findImageFile(paths)
    startAsync(files)

def onClose():
    stopAllTask()
    event.stop()
    master.destroy()

def onRestart():
    pass

def onStop():
    global isTaskInProgress
    isTaskInProgress = False
    stopAllTask()

def _init_master():
    master.title(MAIN_WINDOW_TITLE)
    ws = master.winfo_screenwidth()
    hs = master.winfo_screenheight()
    x = (ws / 2) - (MAIN_WINDOW_SIZE[0] / 2)
    y = (hs / 2) - (MAIN_WINDOW_SIZE[1] / 2)
    master.geometry('%dx%d+%d+%d' %
                    (MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1], x, y))
    master.resizable(0, 0)
    master.protocol("WM_DELETE_WINDOW", onClose)

def _drop(event):
    print(event.data)
    startCompress(event.data)

def showDialog(title, content):
    MessageBox.showinfo(title, content)

def showContact():
    showDialog(u"提示", u"QQ群:825994338")

def showUpdate():
    webbrowser.open("https://pan.baidu.com/s/101-a9cD7lpzJiXCWSql8-Q?pwd=spng")

def _init_log_frame():
    global textLog
    textLog = Tkinter.Text(master,font=(u'微软雅黑', 10))
    textLog.place(x=0, y=0, width=MAIN_WINDOW_SIZE[0], height=DROP_FRAME_HEIGHT)
    textLog.drop_target_register(DND_FILES)
    textLog.dnd_bind('<<Drop>>', _drop)
    showLog(u"拖动文件或文件夹到窗口进行压缩...")

    scroll = Tkinter.Scrollbar(master)
    scroll.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
    scroll.config(command=textLog.yview)
    textLog.config(yscrollcommand=scroll.set)
    
def _init_menu():
    menubar = Tkinter.Menu(master)
    filemenu = Tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=onClose)
    # filemenu.add_command(label="Restart", command=onRestart)
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Stop", command=onStop)
    helpemenu = Tkinter.Menu(menubar, tearoff=0)
    helpemenu.add_command(label="Contact Us", command=showContact)
    helpemenu.add_command(label="Update", command=showUpdate)
    # menubar.add_cascade(label="Help", menu=helpemenu)
    master.config(menu=menubar)

def showLog(log):
    global logQueue
    logQueue.append(log)

def cleanLogText():
    global textLog
    textLog.config(state=Tkinter.NORMAL)
    textLog.delete("1.0", Tkinter.END)
    textLog.config(state=Tkinter.DISABLED)
    if os.path.exists(logFile):
        os.unlink(logFile)

def onTaskFinished():
    global isTaskInProgress
    global taskStartTime
    endTime = time.time()
    writeLog(packLogSendUI("finished..."))
    writeLog(packLogSendUI("spend time:" + str(endTime - taskStartTime)))
    isTaskInProgress = False
    taskStartTime = 0

def showLogToText():
    global logQueue
    if len(logQueue) > 0:
        logs = logQueue
        logQueue = []
        for log in logs:
            try:
                textLog.config(state=Tkinter.NORMAL)
                textLog.insert(Tkinter.END,log+"\n")
                textLog.see(Tkinter.END)
                textLog.config(state=Tkinter.DISABLED)
            except:
                writeLog(packLogNotSendUI("\nexcept:\n"))
                writeLog(packLogNotSendUI(traceback.format_exc()))

def logLoop():
    showLogToText()
    master.after(500, logLoop)
        

def init_ui():
    _init_master()
    logLoop()
    _init_menu()
    _init_log_frame()
    master.mainloop()

def init_event():
    event.on("SHOW_LOG", showLog)
    event.on("CLEAN_LOG", cleanLogText)
    event.on("ALL_TASK_FINISHED", onTaskFinished)
