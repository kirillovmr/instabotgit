from subprocess import Popen, PIPE, call
from datetime import datetime
from sys import platform # mac or linux
import time

# Array of running scripts
running = []

def now_time():
    return "{}:{}:{}".format(datetime.now().hour, datetime.now().minute, datetime.now().second)

# Checking launch platform
if "darwin" in platform.lower():
    path_ = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages"
    print("{} Bot launched on MAC OS".format(now_time()))
elif "linux" in platform.lower():
    path_ = "/usr/local/lib/python3.4/dist-packages"
    print("{} Bot launched on LINUX".format(now_time()))
else:
    print("{} This platform is not supported. Exiting...".format(now_time()))
    exit()

# Return last digit
def lastdigit(int_):
    return int(str(int_)[len(str(int_))-1])

# Return number without last digit
def removelastdigit(int_):
    return int(int_ / 10)

# Return num of script
def scripttonum(script):
    if script == "follow":
        return 1
    elif script == "unfollow":
        return 2
    elif script == "like":
        return 3
    elif script == "comment":
        return 4
    elif script == "direct":
        return 5
    elif script == "repost":
        return 6
    else:
        print("{} ERROR! scripttpnum() func cant parse {} param.".format(now_time(), script))

# Return script name
def numtoscript(int_):
    if int_ == 1:
        return "follow"
    elif int_ == 2:
        return "unfollow"
    elif int_ == 3:
        return "like"
    elif int_ == 4:
        return "comment"
    elif int_ == 5:
        return "direct"
    elif int_ == 6:
        return "repost"
    else:
        print("{} ERROR! numtoscript() func cant parse '{}' param.".format(now_time(), int_))

# Function returns path to script
# script = like, follow, unfollow, comment, direct
def script_path(script, id):
    return "python3 {}/instabot/scripts/{}.py -bot_id={}".format(path_, script, id)

# Function returns path to log file
def logfile(id, script):
    return "{}/instabot/accs/{}/logs/{}.log".format(path_, id, script)

log = dict()
# Opening log file with write option
def openlog(id, script):
    log[id] = dict() # making it 2d
    log[id][script] = open(logfile(id, script), 'a')
    return log[id][script]

procs = dict()
# Starting python script
def start(id, script):
    # Making array 2d only once
    try:
        type(procs[id])
    except KeyError:
        procs[id] = dict() # making it 2d

    procs[id][script] = Popen(script_path(script, id), shell=True, stdout=openlog(id, script), stderr=PIPE)
    # procs[id][script] = call(script_path(script, id), shell=True)
    if procs[id][script].poll() == None:
        print("{} Bot {}-'{}' was started successfully. PID: {}".format(now_time(), id, script.upper(), procs[id][script].pid))
        running.append(id * 10 + scripttonum(script))

# Stopping python script
def stop(id, script):
    procs[id][script].kill()
    print("{} Bot {}-'{}' was stopped by request.".format(now_time(), id, script.upper()))
    running.remove(id * 10 + scripttonum(script))

# Check are scripts still running. If no - restarts
def checkrun():
    for num in running:
        id = removelastdigit(num)
        script = numtoscript(lastdigit(num))
        if procs[id][script].poll() != None:
            running.remove(num)
            print("{} Bot {}-'{}' was closed. Trying to restart...".format(now_time(), id, script.upper()))
            start(id, script)

# Print working scripts
def print_running():
    print("{} NOW RUNNING:".format(now_time()))
    for num in running:
        id = removelastdigit(num)
        script = numtoscript(lastdigit(num))
        print("Bot {} - {}". format(id, script.upper()))

def print_running_array():
    print("{} Running: {}".format(now_time(), sorted(running)))
