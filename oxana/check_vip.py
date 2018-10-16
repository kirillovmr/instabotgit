import os
import sys
import argparse
import huepy # for color print
from datetime import datetime
from tqdm import tqdm
import func

# Объявляем переменные
bad_users = {}
followers_id_name = {}

# Приветственное сообщение
print(func.hello.format(func.scriptName['check_vip']))

# Выводит платформу
print("\tЗапущено на платформе " +  func.getOs() + "\n")
path_ = func.getPath()
if path_ == None:
    print("This platform is not supported. Exiting...")
    exit()

# Подключаем бота
sys.path.append(path_)
from instabot import Bot, utils

# Создаем папки
dir = "{}/accs/{}/a".format(path_, func.login)
dir0 = "{}/accs/{}".format(path_, func.login)
if not os.path.exists(dir):
    os.makedirs(dir)
if not os.path.exists(dir0 + '/vips'):
    os.makedirs(dir0 + '/vips')

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

# Считываем список ВИПОВ
vip = bot.read_list_from_file('../' + func.vip_filename)
# Удаляем повторяющиеся элементы
vip = list(set(vip))
# Конвертируем usernames to id
vip_id = []
for v in vip:
    vip_id.append(bot.convert_to_user_id(v))

# Получаем список пользователей которых нужно проверить
check_users = bot.read_list_from_file('../' + func.check_users_filename)
# Удаляем повторяющиеся элементы
check_users = list(set(check_users))
# Конвертируем usernames to id
check_users_id = []
for c in check_users:
    check_users_id.append(bot.convert_to_user_id(c))

# Получаем список подписчиков
followers = bot.followers

# Убираем випов из подписчиков
users_to_check = [x for x in followers if x not in vip_id]

# Получаем подписчиков випов
print("ПОЛУЧАЕМ ПОДПИСЧИКОВ ВИПОВ")
vips_to_check = {}
for v in vip_id:
    vips_to_check[v] = bot.get_user_followers(v)
for c in check_users_id:
    vips_to_check[c] = bot.get_user_followers(c)

# Проверяем подписки на випов
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

# Конвертация
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

# Сохраняем словарь usernames
f = open('usernames.txt', 'w')
for u in followers_id_name:
    f.write(u + ':' + followers_id_name[u] + '\n')
f.close()

# Экспортируем результаты
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

func.console_print('\n\tКоличество аккаунтов не выполнивших условия: {}\n'.format(len(bad_users)), color='purple')
func.console_print('Результаты сохранены в файле {}\n'.format(result_filename), color='purple')
input("")
