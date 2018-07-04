import os
import sys
import argparse
from sys import platform # mac or linux
import huepy # for color print
from datetime import datetime
from tqdm import tqdm

hello = '''
    _________________________________________

      INSTAGRAM Hashtag-user by @kirillovmr
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
proxy = "http://oxanaroma:A0z2CkV@31.41.219.235:65233"
post_link = "https://www.instagram.com/p/"
result_filename = 'result.txt'
vip_filename = 'vip.txt'

# Creating folders
dir = "{}/accs/{}/a".format(path_, login)
dir0 = "{}/accs/{}".format(path_, login)
if not os.path.exists(dir):
    os.makedirs(dir)
if not os.path.exists(dir0 + '/hashtag_authors'):
    os.makedirs(dir0 + '/hashtag_authors')

# Changing directory to instabot/accs/bot_id
os.chdir(dir)

bot = Bot()
bot.login(username=login, password=password, proxy=proxy)

users_posted = []
usernames_posted = []

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

# Getting followers
followers = bot.followers

h = bot.get_total_hashtag_medias(hashtag, amount=amount, filtration=False)
# Deleting repeated items
posts = list(set(h))

# users_to_check = users_to_check[0:10]
# posts = posts[0:10]

# Получаем список авторов всех фото в хештеге
for post in tqdm(posts, desc="Получаем список авторов"):
    users_posted.append(bot.get_media_owner(post))

for u in tqdm(users_posted, desc="Конвертация"):
    id = u
    try:
        username = followers_id_name[id]
    except KeyError:
        username = bot.get_username_from_user_id(id)
        followers_id_name[id] = username
    usernames_posted.append(username)

# Saving usernames dict
f = open('usernames.txt', 'w')
for u in followers_id_name:
    f.write(u + ':' + followers_id_name[u] + '\n')
f.close()

# Export results in file
date = datetime.today().strftime("%d.%m.%Y %H;%M")
result_filename = date + '.txt'
f = open('../hashtag_authors/' + result_filename, 'w')
f.write("Отчет авторов публикаций по хештегу #{}\n".format(hashtag))
f.write("Сгенерирован {}\n\n".format(date))

for u in usernames_posted:
    f.write(u + "\n")
f.close()

console_print('\nРезультаты сохранены в файле {}\n'.format(result_filename), color='purple')
input("")
