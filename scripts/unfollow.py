"""
    Bot - Unfollow everyone
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

print("SETTINGS: unfollow_delay: {}, per_day: {}".format(settings['unfollow_delay'], settings['max_unfollows_per_day']))

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot(script='unfollow', max_unfollows_per_day=settings['max_unfollows_per_day'], unfollow_delay=settings['unfollow_delay'])
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

bot.unfollow_everyone()
