"""
    Bot - Comment medias by location
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
elif "win32" in platform.lower():
    print("Script launched on WINDOWS")
    path_ = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\instabot"
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
comments = my_database.get_comments(args.bot_id)
settings['comment_delay'] = round( (24*60*60)/settings['max_comments_per_day'] )

# Receiving proxy from new table
new_proxy = my_database.get_new_proxy(settings['login'])
if new_proxy:
    settings['proxy'] = new_proxy

# Closing connection to database
my_database.db['cnx'].close()

# Mixing array
random.shuffle(comments)

print("SETTINGS: comment_location: '{}', comment_delay: {}s".format(settings['location'], settings['comment_delay']))
comments_sent = 0

# Func from examples/commenr_medias_by_location.py
def comment_location_feed(new_bot, new_location, amount=0):
    srez = random.randint(0, 4)
    num = comments_sent % len(comments)
    counter = 0
    max_id = ''
    with tqdm(total=amount) as pbar:
        while counter < amount:
            if new_bot.api.get_location_feed(new_location['location']['pk'], max_id=max_id):
                location_feed = new_bot.api.last_json
                for media in new_bot.filter_medias(location_feed["items"][srez:srez+amount], quiet=True):
                    if bot.comment(media, comments[num]):
                        bot.logger.info("Commented {}".format(comments[num]))
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

bot = Bot(script='comment', comment_delay=settings['comment_delay'])
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

ncomments = 1
start_time = datetime.datetime.now()

while True:
    bot.api.search_location(settings['location'])
    if not bot.api.last_json['items']:
        print(u'Location was not found')
        exit(1)
    try:
        # First location in found array
        ans = 0
        if ans in range(len(bot.api.last_json["items"])):
            comment_location_feed(bot, bot.api.last_json["items"][ans], amount=int(ncomments))
            comments_sent += 1
            print('{now} WAITING {wait}s. | {comments_sent} comments posted. | Working {working}.'.format(
                now=now_time(), wait=settings['comment_delay'], comments_sent=comments_sent, working=datetime.datetime.now() - start_time))
            time.sleep(settings['comment_delay'] + random.randint(-30, 30))
    except ValueError:
        print(u"\n Not valid choice. Try again")
