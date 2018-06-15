"""
    Bot - Follow user followers
"""
import os
import sys
import time
import random
import argparse
from sys import platform # mac or linux

if "darwin" in platform.lower():
    print("Script launched on MAC OS")
    path_ = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/instabot"
elif "linux" in platform.lower():
    print("Script launched on LINUX")
    path_ = "/usr/local/lib/python3.4/dist-packages/instabot"
else:
    print("This platform is not supported. Exiting...")
    exit()

sys.path.append(os.path.join(sys.path[0], '../'))
sys.path.append(path_)
from instabot import Bot
import my_database

# Parsing arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-bot_id', type=int, help="bot_id")
args = parser.parse_args()

# Receiving settings for acc
settings = my_database.get_settings(args.bot_id)

# Putting donor accounts in array
accs_tmp = settings['follow_followers']
accs = [] # Initializing empty array
while accs_tmp.find(" ") >= 0:
    pos = accs_tmp.find(" ")
    accs.append(accs_tmp[:pos])
    accs_tmp = accs_tmp[pos+1:]
accs.append(accs_tmp) # Appending to array last hashtag

print("SETTINGS: follow_followers_of: {}, delay: {}, per_day: {}".format(accs, settings['follow_delay'], settings['max_follows_per_day']))

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot(max_follows_per_day=settings['max_follows_per_day'],
        follow_delay=settings['follow_delay'], max_following_to_followers_ratio=4,
        max_followers_to_following_ratio=20, filter_business_accounts=False,
        max_followers_to_follow=5000, max_following_to_follow=7500)
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

for username in accs:
    bot.follow_followers(username)
