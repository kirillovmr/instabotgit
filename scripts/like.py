"""
    Bot - Infinity hashtags liker.
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

# Putting hashtags in array
hashtags_tmp = settings['like_hashtags']
hashtags = [] # Initializing empty array
while hashtags_tmp.find(" ") >= 0:
    pos = hashtags_tmp.find(" ")
    hashtags.append(hashtags_tmp[:pos])
    hashtags_tmp = hashtags_tmp[pos+1:]
hashtags.append(hashtags_tmp) # Appending to array last hashtag

# Mixing array
random.shuffle(hashtags)

print("SETTINGS: max_likes: {}, delay: {}".format(settings['max_likes_per_day'], settings['like_delay']))

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot(script='like', max_likes_per_day=settings['max_likes_per_day'], like_delay=settings['like_delay'])
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

wait = 5 * 60  # in seconds | Waiting between each hashtag

while True:
    for hashtag in hashtags:
        bot.like_hashtag(hashtag)
        time.sleep(wait)
        exit(10)
