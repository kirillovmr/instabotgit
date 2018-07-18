"""
    Bot - Repost best photo from user
"""
import os
import sys
import time
import random
import argparse
import subprocess
from tqdm import tqdm
from sys import platform # mac or linux
from datetime import datetime

posted = 0

sys.path.append(os.path.join(sys.path[0], '../'))

import my_func
path_ = my_func.path()

sys.path.append(path_)
from instabot import Bot
from instabot.bot.bot_support import read_list_from_file
import my_database
from my_func import now_time

USERNAME_DATABASE = 'username_database.txt'
POSTED_MEDIAS = 'posted_medias.txt'

last_medias_id = []

# Return time of last photo posted
def last_post_time():
    medias = bot.get_your_medias()
    info = bot.get_media_info(medias[0])

    timestamp = info[0]['taken_at']
    time = datetime.fromtimestamp(int(timestamp))
    return time

# Return difference between 2 datetime in minutes
def difference_in_minutes(time1, time2):
    time1_unix = time.mktime(time1.timetuple())
    time2_unix = time.mktime(time2.timetuple())
    time_difference = int(time2_unix - time1_unix) / 60
    return time_difference

# Functions copied from examples/repost_best_photos_from_users.py
def repost_best_photos(bot, users, amount=1):
    medias = get_not_used_medias_from_users(bot, users)
    medias = sort_best_medias(bot, medias, amount)
    for media in tqdm(medias, desc='Reposting photos'):
        if repost_photo(bot, media):
            print("ok")
        else:
            update_posted_medias(media, POSTED_MEDIAS)
            print("nope")

def sort_best_medias(bot, media_ids, amount=1):
    best_medias = [bot.get_media_info(media)[0] for media in tqdm(media_ids, desc='Getting media info')]
    try:
        best_medias = sorted(best_medias, key=lambda x: (x['like_count'], x['comment_count']), reverse=True)
    except KeyError:
        print("key error")
        best_medias = sorted(best_medias, key=lambda x: (x['like_count']), reverse=True)
    return [best_media['pk'] for best_media in best_medias[:amount]]

def get_not_used_medias_from_users(bot, users=None, users_path=USERNAME_DATABASE):
    if not users:
        users = read_list_from_file(users_path)
    users = map(str, users)
    total_medias = []
    for user in users:
        if user == settings['login']:
            medias = bot.get_user_tags_medias(bot.convert_to_user_id(user))
        else:
            medias = bot.get_user_medias(user, filtration=False)
        medias = [media for media in medias if not exists_in_posted_medias(media)]
        total_medias.extend(medias)
    return total_medias

def exists_in_posted_medias(new_media_id, path=POSTED_MEDIAS):
    medias = read_list_from_file(path)
    return str(new_media_id) in medias

def update_posted_medias(new_media_id, path=POSTED_MEDIAS):
    medias = read_list_from_file(path)
    medias.append(str(new_media_id))
    with open(path, 'w') as file:
        file.writelines('\n'.join(medias))
    return True

def repost_photo(bot, new_media_id, path=POSTED_MEDIAS):
    if exists_in_posted_medias(new_media_id, path):
        bot.logger.warning("Media {0} was uploaded earlier".format(new_media_id))
        return False
    photo_path = download_photo(media_id=new_media_id, save_description=True)
    time.sleep(5)
    if not photo_path or not isinstance(photo_path, str):
        # photo_path could be True, False, or a file path.
        return False
    try:
        with open(photo_path[:-3] + 'txt', 'r', encoding="utf8") as f:
            text = ''.join(f.readlines())
        if bot.upload_photo(photo_path, text):
            update_posted_medias(new_media_id, path)
            bot.logger.info('Media_id {0} is saved in {1}'.format(new_media_id, path))
            return True
        else:
            print("not posted")
    except TypeError:
        update_posted_medias(new_media_id, path)
        bot.logger.info('ERROR. Ignore this photo')

# Return @username or -1
def return_author(your_text):
    if your_text.find("@") != -1:
        index1 = your_text.find("@")
        new_text = your_text[index1:]
        index = []
        if new_text.find(" ") != -1:
            index.append(new_text.find(" ")) # simple space
        if new_text.find("⠀") != -1:
            index.append(new_text.find("⠀")) # insta space
        if new_text.find("\n") != -1:
            index.append(new_text.find("\n"))# enter

        if(len(index) > 0):
            index = sorted(index)
            new_text = new_text[:index[0]]
        return new_text
    else:
        return -1

# Return edited caption
def edit_caption(your_text):
    author = return_author(your_text)
    if author != -1:
        caption = user_caption.format(author)
    else:
        caption = user_caption.format("@{}".format(settings["login"]))
    return caption

# Function from bot/bot_photo.py
def download_photo(media_id, folder='photos', filename=None, save_description=False):
    bot.small_delay()
    if not os.path.exists(folder):
        os.makedirs(folder)
    if save_description:
        media = bot.get_media_info(media_id)[0]

        caption = media['caption']['text']
        username = media['user']['username']

        # Checking if reposting from self tags feed
        if users[posted % len(users)] == settings['login']:
            caption = user_caption.format("@" + username)
        else:
            caption = edit_caption(caption)

        fname = os.path.join(folder, '{}_{}.txt'.format(username, media_id))
        with open(fname, encoding='utf8', mode='w') as f:
            f.write(caption)
    try:
        return bot.api.download_photo(media_id, filename, False, folder)
    except Exception:
        bot.logger.info("Media with `{}` is not downloaded.".format(media_id))
        return False

# Parsing arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-bot_id', type=int, help="bot_id")
args = parser.parse_args()

# Receiving settings for acc
settings = my_database.get_settings(args.bot_id)
user_caption = settings["caption"]

# Receiving proxy from new table
new_proxy = my_database.get_new_proxy(settings['login'])
if new_proxy:
    settings['proxy'] = new_proxy

# Closing connection to database
my_database.db['cnx'].close()

# Putting donors in array
users_tmp = settings['donors']
users = [] # Initializing empty array
user = [] # Required!
while users_tmp.find(" ") >= 0:
    pos = users_tmp.find(" ")
    users.append(users_tmp[:pos])
    users_tmp = users_tmp[pos+1:]
# Appending to array last hashtag
users.append(users_tmp)

# Mixing array
random.shuffle(users)

# Setting delay between posts in minutes
delay_between_posts = settings["repost_delay"]
delay_between_posts = 1

print("SETTINGS: delay_between_posts: {} min.".format(settings['repost_delay']))

# Creating folders
dir = "{}/accs/{}/logs".format(path_, args.bot_id)
if not os.path.exists(dir):
    os.makedirs(dir)

# Changing directory to instabot/accs/bot_id
os.chdir("{}/accs/{}".format(path_, args.bot_id))

bot = Bot(script='repost')
bot.login(username=settings['login'], password=settings['password'],
          proxy=settings['proxy'])

# Infinite cycle
while True:
    # Getting the time of last photo posted
    time_post = last_post_time()

    # Getting difference in minutes
    time_difference = difference_in_minutes(time_post, datetime.now())
    # time_difference = 50

    if(time_difference >= delay_between_posts):
        user = []
        user.append(users[posted % len(users)])
        print("{} Difference {} min. | Going to repost from {}".format(now_time(), time_difference, user[0]))
        repost_best_photos(bot, user, 1) # 1 - number of photos to repost
        posted += 1
    else:
        wait_to_next_post = delay_between_posts - time_difference
        print("{} Difference {} min. | Waiting {} min before next post".format(now_time(), time_difference, wait_to_next_post))
        time.sleep(wait_to_next_post * 60)

    time.sleep(10) # waiting required after post
