import os
import sys
import argparse
import huepy # for color print
from datetime import datetime
from tqdm import tqdm
import func

# Объявляем переменные
users_posted = []
usernames_posted = []
followers_id_name = {}

# Приветственное сообщение
print(func.hello.format(func.scriptName['hashtag_users']))

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
if not os.path.exists(dir0 + '/hashtag_authors'):
    os.makedirs(dir0 + '/hashtag_authors')

# Меняем директорию на instabot/accs/bot_id
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

# Получаем список подписчиков
followers = bot.followers

# Получаем список хештегов
h = bot.get_total_hashtag_medias(hashtag, amount=amount, filtration=False)
# Удаляем повторяющиеся елементы
posts = list(set(h))

# Получаем список авторов всех фото в хештеге
for post in tqdm(posts, desc="Получаем список авторов"):
    users_posted.append(bot.get_media_owner(post))
# Удаляем повторяющиеся елементы
users_posted = list(set(users_posted))

# Убираем не подписчиков из users_posted
users_posted = [x for x in users_posted if x in followers]

for u in tqdm(users_posted, desc="Конвертация"):
    id = u
    try:
        username = followers_id_name[id]
    except KeyError:
        username = bot.get_username_from_user_id(id)
        followers_id_name[id] = username
    usernames_posted.append(username)

# Сохраняем словарь usernames
f = open('usernames.txt', 'w')
for u in followers_id_name:
    f.write(u + ':' + followers_id_name[u] + '\n')
f.close()

# Экспортируем результаты
date = datetime.today().strftime("%d.%m.%Y %H;%M")
result_filename = date + '.txt'
f = open('../hashtag_authors/' + result_filename, 'w')
f.write("Отчет авторов публикаций по хештегу #{}\n".format(hashtag))
f.write("Сгенерирован {}\n".format(date))
f.write("Пользователей: {}\n\n".format(len(usernames_posted)))

for u in usernames_posted:
    f.write(u + "\n")
f.close()

func.console_print('\nРезультаты сохранены в файле {}\n'.format(result_filename), color='purple')
input("")
