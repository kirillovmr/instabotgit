import subprocess, time, datetime

process_responce = {}

path = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/instabot/test3.py"

process = subprocess.Popen('python3 {}'.format(path), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

# def check_response(proc):


while True:
    print(process.poll())
    time.sleep(1)
