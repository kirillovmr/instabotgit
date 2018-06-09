from subprocess import Popen, PIPE
from sys import platform # mac or linux
import time

# Checking launch platform
if "darwin" in platform.lower():
    path_ = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages"
    print("Bot launched on MAC OS")
elif "linux" in platform.lower():
    path_ = "/usr/local/lib/python3.4/dist-packages"
    print("Bot launched on LINUX")
else:
    print("This platform is not supported. Exiting...")
    exit()

# Array of running scripts
running = []

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
    else:
        print("ERROR! scripttpnum() func cant parse {} param.".format(script))

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
    else:
        print("ERROR! numtoscript() func cant parse '{}' param.".format(int_))

# Function returns path to script
# script = like, follow, unfollow, comment, direct
def script_path(script):
    return "python3 {}/instabot/scripts/{}.py".format(path_, script)

# Function returns path to log file
def logfile(id, script):
    return "{}/instabot/accs/{}/{}.log".format(path_, id, script)

log = dict()
# Opening log file with write option
def openlog(id, script):
    log[id] = dict() # making it 2d
    log[id][script] = open(logfile(id, script), 'w')
    return log[id][script]

procs = dict()
# Starting python script
def start(id, script):
    procs[id] = dict() # making it 2d
    procs[id][script] = Popen(script_path(script), shell=True, stdout=openlog(id, script), stderr=PIPE)
    if procs[id][script].poll() == None:
        print("Bot {}-'{}' was started successfully. PID: {}".format(id, script, procs[id][script].pid))
        running.append(id * 10 + scripttonum(script))

# Check are scripts still running
def checkrun():
    for num in running:
        ## procs[id][script]
        if procs[removelastdigit(num)][numtoscript(lastdigit(num))].poll() != None:
            running.remove(num)
            print("Bot {}-'{}' was closed".format(removelastdigit(num), numtoscript(lastdigit(num))))


start(1, "like")
start(2, "follow")

while(len(running)):
    checkrun()
    print(running)
    time.sleep(1)
