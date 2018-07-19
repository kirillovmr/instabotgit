"""
    Bot - Follow user followers
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

if settings['follow_type'] == 1:
    # FOLLOW BY LOCATION
    # Putting locations in array
    locations_tmp = settings['location']
    locations = [] # Initializing empty array
    while locations_tmp.find(" ") >= 0:
        pos = locations_tmp.find(" ")
        locations.append(locations_tmp[:pos])
        locations_tmp = locations_tmp[pos+1:]
    locations.append(locations_tmp) # Appending to array last hashtag

elif settings['follow_type'] == 2:
    # FOLLOW BY HASHTAGS
    print()

elif settings['follow_type'] == 3:
    # FOLLOW BY DONORS
    # Putting donor accounts in array
    accs_tmp = settings['follow_followers']
    accs = [] # Initializing empty array
    while accs_tmp.find(" ") >= 0:
        pos = accs_tmp.find(" ")
        accs.append(accs_tmp[:pos])
        accs_tmp = accs_tmp[pos+1:]
    accs.append(accs_tmp) # Appending to array last hashtag

print("SETTINGS: delay: {}, per_day: {}".format(settings['follow_delay'], settings['max_follows_per_day']))

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot(script='follow', max_follows_per_day=settings['max_follows_per_day']+100,
        follow_delay=settings['follow_delay'], max_following_to_followers_ratio=4,
        max_followers_to_following_ratio=20, filter_business_accounts=False,
        max_followers_to_follow=5000, max_following_to_follow=7500, stop_words='')
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

if settings['follow_type'] == 1:
    bot.logger.info("=== SCRIPT 'FOLLOW BY LOCATION' ===")
    while True:
        for location in locations:
            print("Location: {}".format(location))
            bot.api.search_location(location)
            loc = random.randint(0, 6)
            for l in bot.api.last_json['items'][:6]:
                try:
                    print(l['title'])
                except UnicodeEncodeError:
                    print("*cant_decode")
            finded_location = bot.api.last_json['items'][loc]
            if finded_location:
                print("Found {}".format(finded_location['title']))
                follow_location_feed(bot, finded_location, amount=int(18))
                time.sleep(settings['follow_delay'])
            else:
                bot.logger.info("FOLLOW_LOCATION | Location '{}' was not found.".format(location))
        exit(10)

elif settings['follow_type'] == 2:
    bot.logger.info("=== SCRIPT 'FOLLOW BY HASHTAGS' ===")

elif settings['follow_type'] == 3:
    bot.logger.info("=== SCRIPT 'FOLLOW BY DONORS' ===")
    for username in accs:
        bot.follow_followers(username)
