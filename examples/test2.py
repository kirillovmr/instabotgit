"""
    modified by @kirillovmr

    Workflow:
        Like last images with hashtag.
"""

import argparse
import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot
import my_get_settings

parser = argparse.ArgumentParser(add_help=True)
# parser.add_argument('-u', type=str, help="username")
# parser.add_argument('-p', type=str, help="password")
# parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('hashtags', type=str, nargs='+', help='hashtags')
parser.add_argument('-bot_id', type=str, help="bot_id")
args = parser.parse_args()

# Receiving settings for acc
settings = my_get_settings.get_settings(args.bot_id)

bot = Bot()
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

wait = 5 * 60  # in seconds

print(args.hashtags[1])
