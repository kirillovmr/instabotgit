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
from my_func import now_time
import my_database

# Parsing arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-bot_id', type=int, help="bot_id")
args = parser.parse_args()

# Receiving settings for acc
settings = my_database.get_settings(args.bot_id)

location_array = []
location_array.append(settings['comment_location'])

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

bot = Bot(max_follows_per_day=settings['max_follows_per_day'],
        follow_delay=settings['follow_delay'], max_following_to_followers_ratio=4,
        max_followers_to_following_ratio=20, filter_business_accounts=False,
        max_followers_to_follow=5000, max_following_to_follow=7500)
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

while True:
    for location in location_array:
        print(u"Location: {}".format(location))
        bot.api.search_location(location)
        finded_location = bot.api.last_json['items'][0]
        if finded_location:
            print(u"Found {}".format(finded_location['title']))
            follow_location_feed(bot, finded_location, amount=int(1))
            time.sleep(settings['follow_delay'])
        else:
            bot.logger.info("FOLLOW_LOCATION | Location '{}' was not found.".format(location))
