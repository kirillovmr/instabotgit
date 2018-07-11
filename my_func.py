from subprocess import Popen, PIPE, call
from datetime import datetime
from sys import platform # mac or linux
import my_telegram
import my_database
import time
import json
import os

# Array of running scripts
running = []

feedback_required = {}

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

# Return True or False if needed to notify via telegram
def need_notify(not_notify, num):
    try:
        index = not_notify.index(num)
        not_notify.pop(index)
        return False
    except ValueError:
        return True

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

def scripttosmile(script):
    if script == "follow":
        return '👤'
    elif script == "unfollow":
        return '👤'
    elif script == "like":
        return '♥️'
    elif script == "comment":
        return '💬'
    elif script == "direct":
        return '✉️'
    elif script == "repost":
        return '📣'
    else:
        return ''

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

    # Creating folders
    dir = "{}/instabot/accs/{}/logs".format(path_, id)
    if not os.path.exists(dir):
        os.makedirs(dir)

    log[id][script] = open(logfile(id, script), 'a')
    return log[id][script]

procs = dict()
# Starting python script
def start(id, script, restart_manual=False, restart_error=False, tg_notify=True):
    # Making array 2d only once
    try:
        type(procs[id])
    except KeyError:
        procs[id] = dict() # making it 2d

    procs[id][script] = Popen(script_path(script, id), shell=True, stdout=openlog(id, script), stderr=PIPE)
    # procs[id][script] = call(script_path(script, id), shell=True)
    if procs[id][script].poll() == None:
        print("{} Bot {}-'{}' was started successfully. PID: {}".format(now_time(), id, script.upper(), procs[id][script].pid))
        if tg_notify:
            if restart_manual:
                my_telegram.send_mess_tg(my_database.get_chat_ids_tg(id), "{} @{} bot was restarted by request".format(scripttosmile(script.lower()), my_database.get_username_from_id(id)))
            elif restart_error:
                my_telegram.send_mess_tg(my_database.get_chat_ids_tg(id), "{} @{} bot was restarted after error".format(scripttosmile(script.lower()), my_database.get_username_from_id(id)))
            else:
                my_telegram.send_mess_tg(my_database.get_chat_ids_tg(id), "{} @{} bot was started".format(scripttosmile(script.lower()), my_database.get_username_from_id(id)))
        running.append(id * 10 + scripttonum(script))

# Stopping python script
def stop(id, script, r=False, tg_notify=True):
    needRemove = True
    try:
        procs[id][script].kill()
    except KeyError:
        needRemove = False
    if not r:
        print("{} Bot {}-'{}' was stopped by request.".format(now_time(), id, script.upper()))
        if tg_notify:
            my_telegram.send_mess_tg(my_database.get_chat_ids_tg(id), "{} @{} bot stopped by request".format(scripttosmile(script.lower()), my_database.get_username_from_id(id)))
    if needRemove:
        running.remove(id * 10 + scripttonum(script))

# Restarting scripts
def restart(id, script, tg_notify=True):
    print("{} Bot {}-'{}' going to restart by request.".format(now_time(), id, script.upper()))
    stop(id, script, r=True)
    time.sleep(5)
    start(id, script, restart_manual=True)

# Check are scripts still running. If no - restarts
def checkrun():
    for num in running:
        id = removelastdigit(num)
        script = numtoscript(lastdigit(num))
        poll = procs[id][script].poll()
        if poll != None:
            running.remove(num)
            if poll == 10:
                text = "{} Bot {}-'{}' finished cycle. Restarting.".format(now_time(), id, script.upper())
                print(text)
                start(id, script, tg_notify=False)
            elif poll == 11:
                text = "Bot {}-'{}' unfollowed everyone. Bot stopped.".format(id, script.upper())
                print(now_time() + " " + text)
                my_telegram.send_mess_tg(my_database.get_chat_ids_tg(id), "👤 {} bot finished unfollowing. Bot stopped".format(my_database.get_username_from_id(id)))
                my_database.update_db("follow_s", 0, id)
            elif poll == 12:
                try:
                    feedback_required[id]['count'] += 1
                    feedback_required[id]['last_time'] = time.time()
                    feedback_error_count = feedback_required[id]['count']
                    if feedback_error_count == 5 or feedback_error_count % 10 == 0:
                        # Telegram inline keyboard
                        inline_button1 = { "text": 'Stop {s} bot'.format(s=script), "callback_data": '/stop {} {}'.format(my_database.get_username_from_id(id), script) }
                        inline_keyboard = [[inline_button1]]
                        keyboard = { "inline_keyboard": inline_keyboard }
                        markup = json.JSONEncoder().encode(keyboard)

                        my_telegram.send_mess_tg(my_database.get_chat_ids_tg(id), "‼️ @{} {} bot returned 'feedback_required' {} times.".format(my_database.get_username_from_id(id), script, feedback_error_count), replyMarkup=markup)
                except KeyError:
                    feedback_required[id] = {}
                    feedback_required[id]['count'] = 1
                    feedback_required[id]['last_time'] = time.time()
                text = "Bot {}-'{}' returned 'feedback_required'. Restarting.".format(id, script.upper())
                print(now_time() + " " + text)
                start(id, script, tg_notify=False)
                # my_database.update_db("{}_s".format(script.lower()), 0, id)
                # running.remove(id * 10 + scripttonum(script))
            else:
                text = "{} Bot {}-'{}' was closed. Trying to restart...".format(now_time(), id, script.upper())
                print(text)
                # my_telegram.send_mess_tg(my_database.get_chat_ids_tg(id), text)
                start(id, script, restart_error=True)

# Clears a feedback_required array if needed. Used to
def clear_feedback_required():
    for acc in list(feedback_required):
        last_error_time = feedback_required[acc]['last_time']
        now_time = time.time()
        diff = now_time - last_error_time
        if diff > 4:
            feedback_required.pop(acc)
    print(feedback_required)


# Print working scripts
def print_running():
    print("{} NOW RUNNING:".format(now_time()))
    for num in running:
        id = removelastdigit(num)
        script = numtoscript(lastdigit(num))
        print("Bot {} - {}". format(id, script.upper()))

def print_running_array():
    print("{} Running: {}".format(now_time(), sorted(running)))
