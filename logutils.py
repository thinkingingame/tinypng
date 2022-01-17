

def packLog(log, isSendToUI):
    return {"content": log, "isSendToUI": isSendToUI}

def packLogSendUI(log):
    return packLog(log, True)

def packLogNotSendUI(log):
    return packLog(log, False)