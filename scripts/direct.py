"""
    Bot - Send message to new followers
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
from instabot import Bot, utils
from my_func import now_time
import my_database

# Parsing arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-bot_id', type=int, help="bot_id")
args = parser.parse_args()

# Receiving settings for acc
settings = my_database.get_settings(args.bot_id)
messages = my_database.get_messages(args.bot_id)
settings['message_delay'] = round( (24*60*60)/settings['max_messages_per_day'] )

# Receiving proxy from new table
new_proxy = my_database.get_new_proxy(settings['login'])
if new_proxy:
    settings['proxy'] = new_proxy

# Closing connection to database
my_database.db['cnx'].close()

# Mixing array
random.shuffle(messages)

NOTIFIED_USERS_PATH = 'notified_users.txt'

print("SETTINGS: message_delay: {}s, check_new_followers_delay: {}s".format(settings['message_delay'], settings['check_new_followers_delay']))
messages_sent = 0

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot(script='direct')
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

start_time = datetime.datetime.now()

while True:
    messages_sent_now = 0
    messages_sent_before = messages_sent

    # Check on existed file with notified users
    notified_users = utils.file(NOTIFIED_USERS_PATH)
    if not notified_users.list:
        notified_users.save_list(bot.followers)
        print(
            'All followers saved in file {users_path}.\n'
            'In a next time, for all new followers script will send messages.'.format(
                users_path=NOTIFIED_USERS_PATH
            )
        )

    print('Read saved list of notified users. Count: {count}'.format(
        count=len(notified_users)
    ))
    all_followers = bot.followers
    print('Amount of all followers is {count}'.format(
        count=len(all_followers)
    ))

    new_followers = set(all_followers) - notified_users.set
    len_new_followers = len(new_followers)

    if not new_followers:
        print('New followers not found')
        bot._followers = None
        time.sleep(5)
    else:
        print('Found new followers. Count: {count}'.format(count=len_new_followers))
        for follower in tqdm(new_followers):
            num = messages_sent % len(messages)
            if bot.send_message(messages[num], follower):
                notified_users.append(follower)
                messages_sent += 1
                messages_sent_now += 1
                bot.logger.info("DIRECT | Message sent to {}".format(follower))
                if len_new_followers > messages_sent_now:
                    bot.logger.info("DIRECT | Waiting {}s to send next message".format(settings['message_delay']))
                    time.sleep(settings['message_delay'])

    bot.logger.info("DIRECT | Bot sent %s messages, working: %s", messages_sent, datetime.datetime.now() - start_time)

    bot.logger.info("DIRECT | Waiting {}s to check new followers".format(settings['check_new_followers_delay']))
    time.sleep(settings['check_new_followers_delay'])
