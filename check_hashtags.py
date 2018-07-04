import os
import sys
import argparse
from sys import platform # mac or linux
import huepy # for color print
from datetime import datetime
from tqdm import tqdm

hello = '''
    _________________________________________

    INSTAGRAM Follower checker by @kirillovmr
    _________________________________________
'''

print(hello)

if "darwin" in platform.lower():
    print("\tЗапущено на платформе MAC OS\n")
    path_ = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/instabot"
elif "linux" in platform.lower():
    print("\tЗапущено на платформе LINUX\n")
    path_ = "/usr/local/lib/python3.5/dist-packages/instabot"
elif "win32" in platform.lower():
    print("\tЗапущено на платформе WINDOWS\n")
    path_ = "c:\\users\\user\\appdata\\local\\programs\\python\\python37\\lib\\site-packages\\instabot"
else:
    print("This platform is not supported. Exiting...")
    exit()

def console_print(text, color=None):
    if color is not None:
        text = getattr(huepy, color)(text)
    print(text)

hashtag = input(getattr(huepy, "purple")("Введите хештег (без #): "))
amount = int(input(getattr(huepy, "purple")("Введите количество публикаций по хештегу: ")))
print(' ')

sys.path.append(path_)
from instabot import Bot, utils

login = "_friendly_company"
password = "arina4ever699516"
post_link = "https://www.instagram.com/p/"
result_filename = 'result.txt'
vip_filename = 'vip.txt'

# Creating folders
dir = "{}/accs/{}/a".format(path_, login)
dir0 = "{}/accs/{}".format(path_, login)
if not os.path.exists(dir):
    os.makedirs(dir)
if not os.path.exists(dir0 + '/hashtags'):
    os.makedirs(dir0 + '/hashtags')

# Changing directory to instabot/accs/bot_id
os.chdir(dir)

bot = Bot()
bot.login(username=login, password=password, proxy='http://ssalina76:O9q2RqH@93.190.43.139:65233')

# Creating dict of bad users
bad_users = {}

# Loading id -> username dict
followers_id_name = {}
try:
    f = open('usernames.txt', 'r')
    for line in f:
        split = line.split(':')
        id = split[0]
        # обрезаем \n
        split2 = split[1].split('\n')
        username = split2[0]
        followers_id_name[id] = username
    f.close()
except:
    print("Loaded file with usernames was not found.")

# Get list of VIP Users
vip = bot.read_list_from_file('../' + vip_filename)

# Deleting repeated items
vip = list(set(vip))

# Converting usernames to id
vip_id = []
for v in vip:
    vip_id.append(bot.convert_to_user_id(v))

# Getting followers
followers = bot.followers

# Removing vip users from followers
users_to_check = [x for x in followers if x not in vip_id]

h = bot.get_total_hashtag_medias(hashtag, amount=amount, filtration=False)
# Deleting repeated items
posts = list(set(h))

# users_to_check = users_to_check[0:10]
# posts = posts[0:10]

# Получаем список лайков под всеми фото в хештеге
new_posts = []
for post in tqdm(posts, desc="Получаем список лайков"):
    new_posts.append({'post': post, 'likers': bot.get_media_likers(post)})

# for user in users_to_check:
for user in tqdm(users_to_check, desc="Проверяем лайки"):
    for post in new_posts:
        likers = post['likers']
        try:
            likers.index(user)
        except ValueError:
            try:
                bad_users[user]["num"] += 1
                if(len(bad_users[user]["proof"]) < 2):
                    bad_users[user]["proof"].append(post['post'])
            except KeyError:
                bad_users[user] = {}
                bad_users[user]["username"] = user
                bad_users[user]["num"] = 1
                bad_users[user]["proof"] = []
                bad_users[user]["proof"].append(post['post'])

madiaid_code = {}
# [PROOF] Convert media id to link
for u in tqdm(bad_users, desc="Конвертация"):
    id = bad_users[u]["username"]
    try:
        username = followers_id_name[id]
    except KeyError:
        username = bot.get_username_from_user_id(id)
        followers_id_name[id] = username
    bad_users[u]["username"] = username
    proofs_link = []
    for post_id in bad_users[u]["proof"]:
        try:
            code = madiaid_code[post_id]
        except KeyError:
            media_info = bot.get_media_info(post_id)
            code = media_info[0]['code']
            madiaid_code[post_id] = code
        proofs_link.append(post_link + code)
    bad_users[u]["proof"] = proofs_link

# Saving usernames dict
f = open('usernames.txt', 'w')
for u in followers_id_name:
    f.write(u + ':' + followers_id_name[u] + '\n')
f.close()

# Export results in file
date = datetime.today().strftime("%d.%m.%Y %H;%M")
result_filename = date + '.txt'
f = open('../hashtags/' + result_filename, 'w')
f.write("Отчет по хештегу #{}\n".format(hashtag))
f.write("Сгенерирован {}\n\n".format(date))

for u in bad_users:
    f.write("{} - {} пропусков.\n".format(bad_users[u]['username'], bad_users[u]['num']))
    for proof in bad_users[u]["proof"]:
        f.write(proof + '\n')
    f.write('\n\n')
f.close()

console_print('\n\tКоличество аккаунтов не выполнивших условия: {}\n'.format(len(bad_users)), color='purple')
console_print('Результаты сохранены в файле {}\n'.format(result_filename), color='purple')
