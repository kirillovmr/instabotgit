"""
    Bot - Follow users by location
"""
import os
import sys
import time
import random
import datetime
import argparse
from sys import platform # mac or linux

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))

import my_func
path_ = my_func.path()

sys.path.append(path_)
from instabot import Bot
from my_func import now_time
import my_database

# Parsing arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-bot_id', type=int, help="bot_id")
args = parser.parse_args()

# Receiving settings for acc
settings = my_database.get_settings(args.bot_id)
settings['follow_delay'] = round( (24*60*60)/settings['max_follows_per_day'] )

# Closing connection to database
my_database.db['cnx'].close()

location_array = []
location_array.append(settings['location'])

def follow_location_feed(new_bot, new_location, amount=0):
    counter = 0
    max_id = ''
    with tqdm(total=amount) as pbar:
        while counter < amount:
            if new_bot.api.get_location_feed(new_location['location']['pk'], max_id=max_id):
                location_feed = new_bot.api.last_json
                for media in new_bot.filter_medias(location_feed["items"][:amount], quiet=True):
                    author = new_bot.get_media_owner(media)
                    if bot.follow(author):
                        counter += 1
                        pbar.update(1)
                if not location_feed.get('next_max_id'):
                    return False
                max_id = location_feed['next_max_id']
    return True

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot(script='follow_l', max_follows_per_day=settings['max_follows_per_day']+100,
        follow_delay=settings['follow_delay'], max_following_to_followers_ratio=4,
        max_followers_to_following_ratio=20, filter_business_accounts=False,
        max_followers_to_follow=5000, max_following_to_follow=7500)
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

while True:
    for location in location_array:
        print("Location: {}".format(location))
        bot.api.search_location(location)
        finded_location = bot.api.last_json['items'][0]
        if finded_location:
            print("Found {}".format(finded_location['title']))
            follow_location_feed(bot, finded_location, amount=int(18))
            time.sleep(settings['follow_delay'])
        else:
            bot.logger.info("FOLLOW_LOCATION | Location '{}' was not found.".format(location))
