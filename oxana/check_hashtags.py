import os
import sys
import argparse
from sys import platform # mac or linux
import huepy # for color print
from datetime import datetime
from tqdm import tqdm
import func

# Объявляем переменные
bad_users = {}
followers_id_name = {}
madiaid_code = {}

# Приветственное сообщение
print(func.hello.format(func.scriptName['check_hashtags']))

# Выводит платформу
print("\tЗапущено на платформе " +  func.getOs() + "\n")
path_ = func.getPath()
if path_ == None:
    print("This platform is not supported. Exiting...")
    exit()

# Получаем вводные данные
hashtag = input(getattr(huepy, "purple")("Введите хештег (без #): "))
amount = int(input(getattr(huepy, "purple")("Введите количество публикаций по хештегу: ")))
print(' ')

# Подключаем бота
sys.path.append(path_)
from instabot import Bot, utils

# Создаем папки
dir = "{}/accs/{}/a".format(path_, func.login)
dir0 = "{}/accs/{}".format(path_, func.login)
if not os.path.exists(dir):
    os.makedirs(dir)
if not os.path.exists(dir0 + '/hashtags'):
    os.makedirs(dir0 + '/hashtags')

# Меняем директорию to instabot/accs/bot_id
os.chdir(dir)

bot = Bot()
bot.login(username=func.login, password=func.password, proxy=func.proxy)

# Loading id -> username dict
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

# Получаем список ВИПОВ
vip = bot.read_list_from_file('../' + func.vip_filename)
# Удаляем повторяющиеся имена
vip = list(set(vip))

# Конвертируем usernames to id
vip_id = []
for v in vip:
    vip_id.append(bot.convert_to_user_id(v))

# Получаем список подписчиков
followers = bot.followers

# Убираем ВИПОВ из followers
users_to_check = [x for x in followers if x not in vip_id]

h = bot.get_total_hashtag_medias(hashtag, amount=amount, filtration=False)
# Удаляем повторяющиеся имена
posts = list(set(h))

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
        proofs_link.append(func.post_link + code)
    bad_users[u]["proof"] = proofs_link

# Сохраняем словарь usernames
f = open('usernames.txt', 'w')
for u in followers_id_name:
    f.write(u + ':' + followers_id_name[u] + '\n')
f.close()

# Экспортируем результаты
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

func.console_print('\n\tКоличество аккаунтов не выполнивших условия: {}\n'.format(len(bad_users)), color='purple')
func.console_print('Результаты сохранены в файле {}\n'.format(result_filename), color='purple')
input("")
