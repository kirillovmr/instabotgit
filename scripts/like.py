"""
    Bot - Infinity location liker.
"""
import os
import sys
import time
import random
import argparse
from sys import platform # mac or linux

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))

import my_func
path_ = my_func.path()

sys.path.append(path_)
from instabot import Bot
import my_database

def like_location_feed(new_bot, new_location, amount=0):
    counter = 0
    max_id = ''
    with tqdm(total=amount) as pbar:
        while counter < amount:
            if new_bot.api.get_location_feed(new_location['location']['pk'], max_id=max_id):
                location_feed = new_bot.api.last_json
                for media in new_bot.filter_medias(location_feed["items"][:amount], quiet=True):
                    print(media)
                    if bot.like(media):
                        counter += 1
                        pbar.update(1)
                if not location_feed.get('next_max_id'):
                    return False
                max_id = location_feed['next_max_id']
    return True

# Parsing arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-bot_id', type=int, help="bot_id")
args = parser.parse_args()

# Receiving settings for acc
settings = my_database.get_settings(args.bot_id)
settings['like_delay'] = round( (24*60*60)/settings['max_likes_per_day'] )

# Closing connection to database
my_database.db['cnx'].close()

# FOLLOW BY LOCATION
# Putting locations in array
locations_tmp = settings['location']
locations = [] # Initializing empty array
while locations_tmp.find(" ") >= 0:
    pos = locations_tmp.find(" ")
    locations.append(locations_tmp[:pos])
    locations_tmp = locations_tmp[pos+1:]
locations.append(locations_tmp) # Appending to array last hashtag

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
        print("Location: {}".format(location))
        bot.api.search_location(location)
        finded_location = bot.api.last_json['items'][0]
        if finded_location:
            try:
                print("Found {}".format(finded_location['title']))
            except UnicodeEncodeError:
                print()
            like_location_feed(bot, finded_location, amount=int(18))
            time.sleep(settings['follow_delay'])
        else:
            bot.logger.info("LIKE_LOCATION | Location '{}' was not found.".format(location))
    exit(10)
