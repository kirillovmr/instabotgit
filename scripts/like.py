"""
    Bot - Infinity location liker.
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
settings['like_delay'] = round( (24*60*60)/settings['max_likes_per_day'] )

# Receiving proxy from new table
new_proxy = my_database.get_new_proxy(settings['login'])
if new_proxy:
    settings['proxy'] = new_proxy

# Closing connection to database
my_database.db['cnx'].close()

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

bot = Bot(script='like', max_likes_per_day=settings['max_likes_per_day']+100, like_delay=settings['like_delay'])
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

while True:
    for location in locations:
        print(u"Location: {}".format(location))
        bot.api.search_location(location)
        finded_location = bot.api.last_json['items'][0]
        if finded_location:
            print(u"Found {}".format(finded_location['title']))
            like_location_feed(bot, finded_location, amount=int(18))
            time.sleep(settings['follow_delay'])
        else:
            bot.logger.info("LIKE_LOCATION | Location '{}' was not found.".format(location))
    exit(10)
