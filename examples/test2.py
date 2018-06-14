import os

path_ = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages"

# Function returns path to log file
def logfile(id, script):
    return "{}/instabot/accs/{}/logs/{}.log".format(path_, id, script)

dir = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/instabot/accs/{}/logs"

if not os.path.exists(dir.format(3)):
    os.makedirs(dir.format(3))

log = open(logfile(3, "like"), 'a')
