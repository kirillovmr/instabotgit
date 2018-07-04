import os
import sys
import argparse
from sys import platform # mac or linux
import huepy # for color print
from datetime import datetime
from tqdm import tqdm

hello = '''
    _________________________________________

      INSTAGRAM VIP checker by @kirillovmr
    _________________________________________
'''

print(hello)

if "darwin" in platform.lower():
    print("\tЗапущено на платформе MAC OS\n")
    path_ = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/instabot"
elif "linux" in platform.lower():
    print("\tЗапущено на платформе LINUX\n")
    path_ = "/usr/local/lib/python3.4/dist-packages/instabot"
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

sys.path.append(path_)
from instabot import Bot, utils

login = "_friendly_company"
password = "arina4ever699516"
post_link = "https://www.instagram.com/p/"
result_filename = 'result.txt'
vip_filename = 'vip.txt'
check_users_filename = 'check_follows.txt'

# Creating folders
dir = "{}/accs/{}/a".format(path_, login)
dir0 = "{}/accs/{}".format(path_, login)
if not os.path.exists(dir):
    os.makedirs(dir)
if not os.path.exists(dir0 + '/vips'):
    os.makedirs(dir0 + '/vips')

# Changing directory to instabot/accs/bot_id
os.chdir(dir)

bot = Bot()
bot.login(username=login, password=password)

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

# Get list of Users to check
check_users = bot.read_list_from_file('../' + check_users_filename)
# Deleting repeated items
check_users = list(set(check_users))
# Converting usernames to id
check_users_id = []
for c in check_users:
    check_users_id.append(bot.convert_to_user_id(c))

# Getting followers
followers = bot.followers

# Removing vip users from followers
users_to_check = [x for x in followers if x not in vip_id]

print("ПОЛУЧАЕМ ПОДПИСЧИКОВ ВИПОВ")
vips_to_check = {}
for v in vip_id:
    vips_to_check[v] = bot.get_user_followers(v)
for c in check_users_id:
    vips_to_check[c] = bot.get_user_followers(c)


# users_to_check = users_to_check[0:40]
# posts = posts[0:10]

for user in tqdm(users_to_check, desc="Проверяем подписки на випов"):
    for v in vips_to_check:
        try:
            vips_to_check[v].index(user)
        except ValueError:
            try:
                bad_users[user]['need_to_f'].append(v)
            except KeyError:
                bad_users[user] = {}
                bad_users[user]['need_to_f'] = []
                bad_users[user]['need_to_f'].append(v)
                bad_users[user]["username"] = user

# Convert
for u in tqdm(bad_users, desc="Конвертация"):
    id = bad_users[u]["username"]
    try:
        username = followers_id_name[id]
    except KeyError:
        username = bot.get_username_from_user_id(id)
        followers_id_name[id] = username
    bad_users[u]["username"] = username

    # Меняем id на username в массиве
    new_arr = []
    for i in bad_users[u]['need_to_f']:
        try:
            username = followers_id_name[i]
        except KeyError:
            username = bot.get_username_from_user_id(i)
            followers_id_name[i] = username
        new_arr.append(username)
    bad_users[u]['need_to_f'] = new_arr

# Saving usernames dict
f = open('usernames.txt', 'w')
for u in followers_id_name:
    f.write(u + ':' + followers_id_name[u] + '\n')
f.close()

# Export results in file
date = datetime.today().strftime("%d.%m.%Y %H;%M")
result_filename = date + '.txt'
f = open('../vips/' + result_filename, 'w')
f.write("Отчет по подпискам на випов\n")
f.write("Сгенерирован {}\n\n".format(date))

for u in bad_users:
    f.write("Пользователь {} не подписался на:\n".format(bad_users[u]['username']))
    for v in bad_users[u]["need_to_f"]:
        f.write(v + '\n')
    f.write('\n\n')
f.close()

console_print('\n\tКоличество аккаунтов не выполнивших условия: {}\n'.format(len(bad_users)), color='purple')
console_print('Результаты сохранены в файле {}\n'.format(result_filename), color='purple')
