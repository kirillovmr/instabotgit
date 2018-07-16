from sys import platform # mac or linux
import my_func
import mysql.connector

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
if "win32" in platform.lower():
    table_status = "bot_status"
elif "linux" in platform.lower():
    table_status = "bot_status"

db = {'cnx': 0, 'cursor': 0}
db['cnx'] = mysql.connector.connect(**config)
db['cursor'] = db['cnx'].cursor(buffered=True, dictionary=True)

# Return db dict
def db_connect():
    db1 = {'cnx': 0, 'cursor': 0}
    db1['cnx'] = mysql.connector.connect(**config)
    db1['cursor'] = db1['cnx'].cursor(buffered=True, dictionary=True)
    return db1

def get_username_from_id(id): #working
    get_query = "SELECT login FROM bots WHERE bot_id = {}".format(id)
    db['cursor'].execute(get_query)
    buff = db['cursor']

    for data in buff:
        username = data['login']
    return username

def fill_not_notify_array(): #working
    get_query = "SELECT bot_id, follow_s, like_s, comment_s, direct_s, repost_s FROM {}".format(table_status)
    db['cursor'].execute(get_query)
    array = []
    settings = db['cursor']
    for data in settings:
        id = data['bot_id']
        if data['follow_s'] == 1:
            array.append(id * 10 + 1)
        elif data['follow_s'] == 2:
            array.append(id * 10 + 2)
        if data['like_s'] == 1:
            array.append(id * 10 + 3)
        if data['comment_s'] == 1:
            array.append(id * 10 + 4)
        if data['direct_s'] == 1:
            array.append(id * 10 + 5)
        if data['repost_s'] == 1:
            array.append(id * 10 + 6)
    return array

# Return array with chat_ids for appropriate bot_id
def get_chat_ids_tg(bot_id): #working
    get_query = "SELECT ac.chatid FROM tgacc_chatid ac, tgacc_bot ab WHERE ac.tgacc_id = ab.tgacc_id AND ab.bot_id = {}".format(bot_id)
    db['cursor'].execute(get_query)
    buff = db['cursor']

    chat_ids = []
    for data in buff:
        chat_ids.append(data['chatid'])
    return chat_ids

def get_admin_tg(): #working
    get_query = "SELECT chatid FROM tgacc_chatid WHERE tgacc_chatid.admin = 1"
    db['cursor'].execute(get_query)
    buff = db['cursor']

    chat_ids = []
    for data in buff:
        chat_ids.append(data['chatid'])
    return chat_ids

def get_new_proxy(username): #working
    get_query = "SELECT p.proxy FROM proxy p WHERE p.username='{}'".format(username)
    db['cursor'].execute(get_query)
    buff = db['cursor']

    for data in buff:
        return data['proxy']

# Return dict() with settings for bot_id
def get_settings(bot_id_): #working
    # Executing query, storing answer in 'buff'
    get_query = ("SELECT * FROM bots WHERE bot_id={}".format(bot_id_))
    db['cursor'].execute(get_query)
    buff = db['cursor']

    # Initializing settings dictionary
    settings = dict()

    # Filling settings dict with values from Database
    for data in buff:
        settings = data

    # Returning settings dictionary
    return settings

# Return array with comments for bot_id
def get_comments(bot_id_): #working
    # Executing query, storing answer in 'buff'
    get_query = ("SELECT * FROM bots_comments WHERE bot_id={}".format(bot_id_))
    db['cursor'].execute(get_query)
    buff = db['cursor']

    # Initializing comments array
    comments = []
    # Appending not empty values
    for data in buff:
        for comment in data:
            if comment.strip() != "" and comment != "bot_id":
                comments.append(data[comment].strip())

    # Returning comments array
    return comments

# Return array with messages for bot_id
def get_messages(bot_id_): #working
    # Executing query, storing answer in 'buff'
    get_query = ("SELECT * FROM bots_messages WHERE bot_id={}".format(bot_id_))
    db['cursor'].execute(get_query)
    buff = db['cursor']

    # Initializing messages array
    messages = []
    # Appending not empty values
    for data in buff:
        for message in data:
            if message.strip() != "" and message != "bot_id":
                messages.append(data[message].strip())

    # Returning messages array
    return messages

# Change values in Bot_status table
def update_db(param, value, bot_id):
    q = ("UPDATE {} SET {}={} WHERE bot_id={}".format(table_status, param, value, bot_id))
    db['cursor'].execute(q)
    db['cnx'].commit()
    # print("{} BOT ID {} | Updated {} with value {}".format(my_func.now_time(), bot_id, param, value))

# Set all actual values to 0 in database. Use it after manager restart
def set_actual_zero():
    q = ("UPDATE {} SET follow_a=0, like_a=0, comment_a=0, direct_a=0, repost_a=0".format(table_status))
    db['cursor'].execute(q)
    db['cnx'].commit()
    print("{} DB 'actual' -> 0".format(my_func.now_time()))

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
            if data['like_s'] != data['like_a']:
                if data['like_s'] == 1 and data['like_a'] == 0 :
                    my_func.start(data['bot_id'], "like", tg_notify=my_func.need_notify(not_notify, data['bot_id'] * 10 + 3))
                    update_db("like_a", 1, data['bot_id'])
                elif data['like_s'] == 0 and data['like_a'] == 1:
                    my_func.stop(data['bot_id'], "like")
                    update_db("like_a", 0, data['bot_id'])
                elif (data['like_s'] == 9 and data['like_a'] == 1) or (data['like_s'] == 9 and data['like_a'] == 0):
                    my_func.restart(data['bot_id'], "like")
                    update_db("like_s", 1, data['bot_id'])
                    update_db("like_a", 1, data['bot_id'])
            # REPOST
            if data['repost_s'] != data['repost_a']:
                if data['repost_s'] == 1 and data['repost_a'] == 0:
                    my_func.start(data['bot_id'], "repost", tg_notify=my_func.need_notify(not_notify, data['bot_id'] * 10 + 6))
                    update_db("repost_a", 1, data['bot_id'])
                elif data['repost_s'] == 0 and data['repost_a'] == 1:
                    my_func.stop(data['bot_id'], "repost")
                    update_db("repost_a", 0, data['bot_id'])
                elif (data['repost_s'] == 9 and data['repost_a'] == 1) or (data['repost_s'] == 9 and data['repost_a'] == 0):
                    my_func.restart(data['bot_id'], "repost")
                    update_db("repost_s", 1, data['bot_id'])
                    update_db("repost_a", 1, data['bot_id'])
            # COMMENT
            if data['comment_s'] != data['comment_a']:
                if data['comment_s'] == 1 and data['comment_a'] == 0:
                    my_func.start(data['bot_id'], "comment", tg_notify=my_func.need_notify(not_notify, data['bot_id'] * 10 + 4))
                    update_db("comment_a", 1, data['bot_id'])
                elif data['comment_s'] == 0 and data['comment_a'] == 1:
                    my_func.stop(data['bot_id'], "comment")
                    update_db("comment_a", 0, data['bot_id'])
                elif (data['comment_s'] == 9 and data['comment_a'] == 1) or (data['comment_s'] == 9 and data['comment_a'] == 0):
                    my_func.restart(data['bot_id'], "comment")
                    update_db("comment_s", 1, data['bot_id'])
                    update_db("comment_a", 1, data['bot_id'])
            # DIRECT
            if data['direct_s'] != data['direct_a']:
                if data['direct_s'] == 1 and data['direct_a'] == 0:
                    my_func.start(data['bot_id'], "direct", tg_notify=my_func.need_notify(not_notify, data['bot_id'] * 10 + 5))
                    update_db("direct_a", 1, data['bot_id'])
                elif data['direct_s'] == 0 and data['direct_a'] == 1:
                    my_func.stop(data['bot_id'], "direct")
                    update_db("direct_a", 0, data['bot_id'])
                elif (data['direct_s'] == 9 and data['direct_a'] == 1) or (data['direct_s'] == 9 and data['direct_a'] == 0):
                    my_func.restart(data['bot_id'], "direct")
                    update_db("direct_s", 1, data['bot_id'])
                    update_db("direct_a", 1, data['bot_id'])
            # FOLLOW
            if data['follow_s'] != data['follow_a']:
                if data['follow_s'] == 1 and data['follow_a'] == 0:
                    my_func.start(data['bot_id'], "follow", tg_notify=my_func.need_notify(not_notify, data['bot_id'] * 10 + 1))
                    update_db("follow_a", 1, data['bot_id'])
                elif data['follow_s'] == 0 and data['follow_a'] == 1:
                    my_func.stop(data['bot_id'], "follow")
                    update_db("follow_a", 0, data['bot_id'])
                elif data['follow_s'] == 2 and data['follow_a'] == 0:
                    my_func.start(data['bot_id'], "unfollow", tg_notify=my_func.need_notify(not_notify, data['bot_id'] * 10 + 2))
                    update_db("follow_a", 2, data['bot_id'])
                elif data['follow_s'] == 0 and data['follow_a'] == 2:
                    my_func.stop(data['bot_id'], "unfollow")
                    update_db("follow_a", 0, data['bot_id'])
                elif data['follow_s'] == 2 and data['follow_a'] == 1:
                    my_func.stop(data['bot_id'], "follow")
                    time.sleep(5)
                    start(data['bot_id'], "unfollow")
                    update_db("follow_a", 2, data['bot_id'])
                elif data['follow_s'] == 1 and data['follow_a'] == 2:
                    my_func.stop(data['bot_id'], "unfollow")
                    time.sleep(5)
                    my_func.start(data['bot_id'], "follow")
                    update_db("follow_a", 1, data['bot_id'])
                elif (data['follow_s'] == 9 and data['follow_a'] == 1) or (data['follow_s'] == 9 and data['follow_a'] == 0):
                    my_func.restart(data['bot_id'], "follow")
                    update_db("follow_s", 1, data['bot_id'])
                    update_db("follow_a", 1, data['bot_id'])
                elif (data['follow_s'] == 9 and data['follow_a'] == 2):
                    my_func.restart(data['bot_id'], "unfollow")
                    update_db("follow_s", 2, data['bot_id'])
                    update_db("follow_a", 2, data['bot_id'])
