import argparse
import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot
import my_database

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-bot_id', type=str, help="bot_id")
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

print("SETTINGS: max_likes: {}, delay: {}".format(settings['max_likes_per_day'], settings['like_delay']))

bot = Bot(max_likes_per_day=settings['max_likes_per_day'], like_delay=settings['like_delay'])
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

wait = 5 * 60  # in seconds | Waiting between each hashtag

while True:
    for hashtag in hashtags:
        bot.like_hashtag(hashtag)
    time.sleep(wait)
