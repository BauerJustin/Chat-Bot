# required imports
import datetime

def getTime():
    time = ""

    # get current time
    current_time = datetime.datetime.now()
    hours = current_time.hour
    minutes = current_time.minute
    
    # convert time to AM or PM and put into string
    if hours < 12:
        if hours == 0:
            hours = 12
        time = "{}:{}{} AM".format(hours, minutes//10, minutes%10)
    else:
        if hours > 12:
            hours -= 12
        time = "{}:{}{} PM".format(hours, minutes//10, minutes%10)
    
    return time

def getDate():
    return ""