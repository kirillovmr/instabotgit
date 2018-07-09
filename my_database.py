from sys import platform # mac or linux
import mysql.connector
from my_func import *

config = {
  'user': 'belyy00_ibot',
  'password': 'Kirillov44',
  'host': 'belyy00.mysql.tools',
  'database': 'belyy00_ibot',
  'charset': 'utf8mb4',
  'collation': 'utf8mb4_general_ci'
}

if "darwin" in platform.lower():
    table_status = "bot_status_test"
elif "linux" in platform.lower():
    table_status = "bot_status"

db = {'cnx': 0, 'cursor': 0}
db['cnx'] = mysql.connector.connect(**config)
db['cursor'] = db['cnx'].cursor(buffered=True)

bot_id_col = 0
foll_s_col = 1
like_s_col = 2
comm_s_col = 3
dire_s_col = 4
foll_a_col = 5
like_a_col = 6
comm_a_col = 7
dire_a_col = 8
repo_s_col = 9
repo_a_col = 10

# Return db dict
def db_connect():
    db1 = {'cnx': 0, 'cursor': 0}
    db1['cnx'] = mysql.connector.connect(**config)
    db1['cursor'] = db1['cnx'].cursor(buffered=True)
    return db1

def get_username_from_id(id):
    get_query = "SELECT login FROM bots WHERE bot_id = {}".format(id)
    db['cursor'].execute(get_query)
    buff = db['cursor']

    for data in buff:
        username = data[0]
    return username

def fill_not_notify_array():
    get_query = "SELECT bot_id, follow_s, like_s, comment_s, direct_s, repost_s FROM {}".format(table_status)
    db['cursor'].execute(get_query)
    array = []
    settings = db['cursor']
    for data in settings:
        id = data[0]
        if data[1] == 1:
            array.append(id * 10 + 1)
        elif data[1] == 2:
            array.append(id * 10 + 2)
        if data[2] == 1:
            array.append(id * 10 + 3)
        if data[3] == 1:
            array.append(id * 10 + 4)
        if data[4] == 1:
            array.append(id * 10 + 5)
        if data[5] == 1:
            array.append(id * 10 + 6)
    return array

# Return array with chat_ids for appropriate bot_id
def get_chat_ids_tg(bot_id):
    get_query = "SELECT ac.* FROM tgacc_chatid ac, tgacc_bot ab WHERE ac.tgacc_id = ab.tgacc_id AND ab.bot_id = {}".format(bot_id)
    db['cursor'].execute(get_query)
    buff = db['cursor']

    chat_ids = []
    for data in buff:
        chat_ids.append(data[1])
    return chat_ids

def get_admin_tg():
    get_query = "SELECT chatid FROM tgacc_chatid WHERE tgacc_chatid.admin = 1"
    db['cursor'].execute(get_query)
    buff = db['cursor']

    chat_ids = []
    for data in buff:
        chat_ids.append(data[0])
    return chat_ids

def get_new_proxy(username):
    get_query = "SELECT p.proxy FROM proxy p WHERE p.username='{}'".format(username)
    db['cursor'].execute(get_query)
    buff = db['cursor']

    for data in buff:
        return data[0]

# Return dict() with settings for bot_id
def get_settings(bot_id_):
    # Executing query, storing answer in 'buff'
    get_query = ("SELECT * FROM bots WHERE bot_id={}".format(bot_id_))
    db['cursor'].execute(get_query)
    buff = db['cursor']

    # Initializing settings dictionary
    settings = dict()

    # Filling settings dict with values from Database
    for data in buff:
        settings['login'] = data[1].strip()
        settings['password'] = data[2].strip()
        settings['proxy'] = data[3].strip()
        settings['max_likes_per_day'] = data[4]
        settings['max_follows_per_day'] = data[5]
        settings['max_unfollows_per_day'] = data[6]
        settings['max_comments_per_day'] = data[7]
        settings['like_delay'] = data[8]
        settings['follow_delay'] = data[9]
        settings['unfollow_delay'] = data[10]
        settings['comment_delay'] = data[11]
        settings['message_delay'] = data[12]
        settings['repost_delay'] = data[13]
        settings['check_new_followers_delay'] = data[14]
        settings['follow_limit'] = data[15]
        settings['f_u_autostart'] = data[16]
        settings['follow_type'] = data[17]
        settings['comment_location'] = data[18].strip()
        settings['follow_followers'] = data[19].strip()
        settings['like_hashtags'] = data[20].strip()
        settings['caption'] = data[21].strip()
        settings['donors'] = data[22].strip()

    # Returning settings dictionary
    return settings

# Return array with comments for bot_id
def get_comments(bot_id_):
    # Executing query, storing answer in 'buff'
    get_query = ("SELECT * FROM bots_comments WHERE bot_id={}".format(bot_id_))
    db['cursor'].execute(get_query)
    buff = db['cursor']

    # Initializing comments array
    comments = []
    # Appending not empty values
    for data in buff:
        i = 1
        while i <= 10:
            if data[i].strip() != "":
                comments.append(data[i].strip())
            i += 1

    # Returning comments array
    return comments

# Return array with messages for bot_id
def get_messages(bot_id_):
    # Executing query, storing answer in 'buff'
    get_query = ("SELECT * FROM bots_messages WHERE bot_id={}".format(bot_id_))
    db['cursor'].execute(get_query)
    buff = db['cursor']

    # Initializing messages array
    messages = []
    # Appending not empty values
    for data in buff:
        i = 1
        while i <= 10:
            if data[i].strip() != "":
                messages.append(data[i].strip())
            i += 1

    # Returning messages array
    return messages

# Change values in Bot_status table
def update_db(param, value, bot_id):
    q = ("UPDATE {} SET {}={} WHERE bot_id={}".format(table_status, param, value, bot_id))
    db['cursor'].execute(q)
    db['cnx'].commit()
    print("{} BOT ID {} | Updated {} with value {}".format(now_time(), bot_id, param, value))

# Set all actual values to 0 in database. Use it after manager restart
def set_actual_zero():
    q = ("UPDATE {} SET follow_a=0, like_a=0, comment_a=0, direct_a=0, repost_a=0".format(table_status))
    db['cursor'].execute(q)
    db['cnx'].commit()
    print("{} All actual values were updated to 0.".format(now_time()))

# Get statuses from database and start/stop bots
def get_bots_status(not_notify):
    # Executing query
    get_query = ("SELECT * FROM {}".format(table_status))
    db['cursor'].execute(get_query)

    # Going through status and start/stop appropriate bots
    settings = db['cursor']
    for data in settings:
        if True:
            # LIKES
            if data[like_s_col] != data[like_a_col]:
                if data[like_s_col] == 1 and data[like_a_col] == 0:
                    start(data[bot_id_col], "like", tg_notify=need_notify(not_notify, data[bot_id_col] * 10 + 3))
                    update_db("like_a", 1, data[bot_id_col])
                elif data[like_s_col] == 0 and data[like_a_col] == 1:
                    stop(data[bot_id_col], "like")
                    update_db("like_a", 0, data[bot_id_col])
                elif data[like_s_col] == 9 and data[like_a_col] == 1:
                    restart(data[bot_id_col], "like")
                    update_db("like_s", 1, data[bot_id_col])
            # REPOST
            if data[repo_s_col] != data[repo_a_col]:
                if data[repo_s_col] == 1 and data[repo_a_col] == 0:
                    start(data[bot_id_col], "repost", tg_notify=need_notify(not_notify, data[bot_id_col] * 10 + 6))
                    update_db("repost_a", 1, data[bot_id_col])
                elif data[repo_s_col] == 0 and data[repo_a_col] == 1:
                    stop(data[bot_id_col], "repost")
                    update_db("repost_a", 0, data[bot_id_col])
                elif data[repo_s_col] == 9 and data[repo_a_col] == 1:
                    restart(data[bot_id_col], "repost")
                    update_db("repost_s", 1, data[bot_id_col])
            # COMMENT
            if data[comm_s_col] != data[comm_a_col]:
                if data[comm_s_col] == 1 and data[comm_a_col] == 0:
                    start(data[bot_id_col], "comment", tg_notify=need_notify(not_notify, data[bot_id_col] * 10 + 4))
                    update_db("comment_a", 1, data[bot_id_col])
                elif data[comm_s_col] == 0 and data[comm_a_col] == 1:
                    stop(data[bot_id_col], "comment")
                    update_db("comment_a", 0, data[bot_id_col])
                elif data[comm_s_col] == 9 and data[comm_a_col] == 1:
                    restart(data[bot_id_col], "comment")
                    update_db("comment_s", 1, data[bot_id_col])
            # DIRECT
            if data[dire_s_col] != data[dire_a_col]:
                if data[dire_s_col] == 1 and data[dire_a_col] == 0:
                    start(data[bot_id_col], "direct", tg_notify=need_notify(not_notify, data[bot_id_col] * 10 + 5))
                    update_db("direct_a", 1, data[bot_id_col])
                elif data[dire_s_col] == 0 and data[dire_a_col] == 1:
                    stop(data[bot_id_col], "direct")
                    update_db("direct_a", 0, data[bot_id_col])
                elif data[dire_s_col] == 9 and data[dire_a_col] == 1:
                    restart(data[bot_id_col], "direct")
                    update_db("direct_s", 1, data[bot_id_col])
            # FOLLOW
            if data[foll_s_col] != data[foll_a_col]:
                if data[foll_s_col] == 1 and data[foll_a_col] == 0:
                    start(data[bot_id_col], "follow", tg_notify=need_notify(not_notify, data[bot_id_col] * 10 + 1))
                    update_db("follow_a", 1, data[bot_id_col])
                elif data[foll_s_col] == 0 and data[foll_a_col] == 1:
                    stop(data[bot_id_col], "follow")
                    update_db("follow_a", 0, data[bot_id_col])
                elif data[foll_s_col] == 2 and data[foll_a_col] == 0:
                    start(data[bot_id_col], "unfollow", tg_notify=need_notify(not_notify, data[bot_id_col] * 10 + 2))
                    update_db("follow_a", 2, data[bot_id_col])
                elif data[foll_s_col] == 0 and data[foll_a_col] == 2:
                    stop(data[bot_id_col], "unfollow")
                    update_db("follow_a", 0, data[bot_id_col])
                elif data[foll_s_col] == 2 and data[foll_a_col] == 1:
                    stop(data[bot_id_col], "follow")
                    time.sleep(5)
                    start(data[bot_id_col], "unfollow")
                    update_db("follow_a", 2, data[bot_id_col])
                elif data[foll_s_col] == 1 and data[foll_a_col] == 2:
                    stop(data[bot_id_col], "unfollow")
                    time.sleep(5)
                    start(data[bot_id_col], "follow")
                    update_db("follow_a", 1, data[bot_id_col])
                elif data[foll_s_col] == 9 and data[foll_a_col] == 1:
                    restart(data[bot_id_col], "follow")
                    update_db("follow_s", 1, data[bot_id_col])
                elif data[foll_s_col] == 9 and data[foll_a_col] == 2:
                    restart(data[bot_id_col], "unfollow")
                    update_db("follow_s", 2, data[bot_id_col])
