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

# Function returns path to script
def path(id):
    return "python3 {}/instabot/examples/test{}.py".format(path_, id)

# Function returns path to log file
def logfile(id):
    return "{}/instabot/examples/test{}.log".format(path_, id)

log = dict()
# Opening log file with write option
def openlog(id):
    log[id] = open(logfile(id), 'w')
    return log[id]

procs = dict()
# Starting python script
def start(id):
    procs[id] = Popen(path(id), shell=True, stdout=openlog(id), stderr=PIPE)
    if procs[id].poll() == None:
        print("Process was started successfully. PID: {}".format(procs[id].pid))
        running.append(id)

# Check are scripts still running
def checkrun():
    for id in running:
        if procs[id].poll() != None:
            running.remove(id)
            print("Process {} was closed.".format(id))


start(2)
start(3)

while(len(running)):
    checkrun()
    print(running)
    time.sleep(1)
