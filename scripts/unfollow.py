"""
    Bot - Unfollow everyone
"""
import os
import sys
import time
import random
import argparse
from sys import platform # mac or linux

sys.path.append(os.path.join(sys.path[0], '../'))

import my_func
path_ = my_func.path()

sys.path.append(path_)
from instabot import Bot
import my_database

# Parsing arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-bot_id', type=int, help="bot_id")
args = parser.parse_args()

# Receiving settings for acc
settings = my_database.get_settings(args.bot_id)
settings['follow_delay'] = round( (24*60*60)/settings['max_follows_per_day'] )

# Receiving proxy from new table
new_proxy = my_database.get_new_proxy(settings['login'])
if new_proxy:
    settings['proxy'] = new_proxy

# Closing connection to database
my_database.db['cnx'].close()

print("SETTINGS: unfollow_delay: {}, per_day: {}".format(settings['follow_delay'], settings['max_follows_per_day']))

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot(script='unfollow', max_unfollows_per_day=settings['max_follows_per_day']+100, unfollow_delay=settings['follow_delay'])
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

bot.unfollow_everyone()
# exit(11)
