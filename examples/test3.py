"""
    Bot - Tag people in comments
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

# Closing connection to database
my_database.db['cnx'].close()

comments_sent = 0

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot()
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

# feed = bot.get_your_medias()
# post_to_comment = feed[0]
# print(bot.get_media_info(post_to_comment))
# exit()
# bot.comment(post_to_comment, "#конкурс @kirillovmr")
# time.sleep(3)
# exit()

posts = bot.get_user_medias('gshock_monstr', filtration=False)
post_to_comment = posts[0]
# print(post_to_comment)
# exit()

# Store all Users
users = bot.get_user_likers("black__kherson")
print(len(users))
# exit()
# users = users[:30]

i = 0
comment = "#конкурс{} ".format(i)
for user in users:
    # username = user
    username = bot.get_username_from_user_id(user)
    comment += '@{} '.format(username)
    i += 1
    if i % 9 == 0:
        print(comment)
        bot.comment(post_to_comment, comment)
        comments_sent += 1
        delay = random.randint(12, 17)
        print("пауза {} сек | Оставлено {} комментов".format(delay, comments_sent))
        time.sleep(delay)
        comment = "#конкурс{} ".format(i)

# bot.comment(last_post, comment)
