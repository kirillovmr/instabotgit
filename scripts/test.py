"""
    Bot - Repost best photo from user
"""
import os
import sys
import time
import random
import argparse
import subprocess
from tqdm import tqdm
from sys import platform # mac or linux
from datetime import datetime

posted = 0

if "darwin" in platform.lower():
    print("Script launched on MAC OS")
    path_ = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/instabot"
elif "linux" in platform.lower():
    print("Script launched on LINUX")
    path_ = "/usr/local/lib/python3.4/dist-packages/instabot"
elif "win32" in platform.lower():
    print("Script launched on WINDOWS")
    path_ = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\instabot"
else:
    print("This platform is not supported. Exiting...")
    exit()

sys.path.append(os.path.join(sys.path[0], '../'))
sys.path.append(path_)
from instabot import Bot
from instabot.bot.bot_support import read_list_from_file
import my_database
from my_func import now_time

USERNAME_DATABASE = 'username_database.txt'
POSTED_MEDIAS = 'posted_medias.txt'

# Parsing arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-bot_id', type=int, help="bot_id")
args = parser.parse_args()

# Receiving settings for acc
settings = my_database.get_settings(args.bot_id)
user_caption = settings["caption"]

# Receiving proxy from new table
new_proxy = my_database.get_new_proxy(settings['login'])
if new_proxy:
    settings['proxy'] = new_proxy

# Closing connection to database
my_database.db['cnx'].close()

# Putting donors in array
users_tmp = settings['donors']
users = [] # Initializing empty array
user = [] # Required!
while users_tmp.find(" ") >= 0:
    pos = users_tmp.find(" ")
    users.append(users_tmp[:pos])
    users_tmp = users_tmp[pos+1:]
# Appending to array last hashtag
users.append(users_tmp)

# Mixing array
random.shuffle(users)

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot(script='repost')
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

medias = bot.get_user_tags_medias(bot.convert_to_user_id('rich_kherson'))
print(medias)
