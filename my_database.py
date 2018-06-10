import mysql.connector
from my_func import *

# Variables to login into Database
HOST = 'belyy00.mysql.tools'
USER = 'belyy00_bot'
PASS = 'Kirillov44'
DB = 'belyy00_bot'

# Return dict() with settings for bot_id
def get_settings(bot_id):
    # Connecting to DataBase
    cnx = mysql.connector.connect(host=HOST, user=USER, password=PASS, database=DB)
    cursor = cnx.cursor(buffered=True)

    # Executing query, storing answer in 'buff'
    get_query = ("SELECT * FROM bot_settings WHERE bot_id={}".format(bot_id))
    cursor.execute(get_query)
    buff = cursor

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
        settings['check_new_followers_delay'] = data[13]
        settings['comment_location'] = data[14].strip()
        settings['follow_followers'] = data[15].strip()
        settings['like_hashtags'] = data[16].strip()
        # add comments
        # add messages

    # Closing connection
    cursor.close()
    cnx.close()

    # Returning settings dictionary
    return settings

# Change values in Bot_status table
def update_db(param, value, bot_id):
    # Connecting to DataBase
    cnx = mysql.connector.connect(host=HOST, user=USER, password=PASS, database=DB)
    cursor = cnx.cursor(buffered=True)

    q = ("UPDATE bot_status SET {}={} WHERE bot_id={}".format(param, value, bot_id))
    cursor.execute(q)
    cnx.commit()
    print("BOT ID {} | Updated {} with value {}".format(bot_id, param, value))

    # Closing connection
    cursor.close()
    cnx.close()

# Set all actual values to 0 in database. Use it after manager restart
def set_actual_zero():
    # Connecting to DataBase
    cnx = mysql.connector.connect(host=HOST, user=USER, password=PASS, database=DB)
    cursor = cnx.cursor(buffered=True)

    q = ("UPDATE bot_status SET follow_a=0, like_a=0, comment_a=0, direct_a=0")
    cursor.execute(q)
    cnx.commit()
    print("All actual values were updated to 0.")

    # Closing connection
    cursor.close()
    cnx.close()

# Get statuses from database and start/stop bots
def get_bots_status():
    # Connecting to DataBase
    cnx = mysql.connector.connect(host=HOST, user=USER, password=PASS, database=DB)
    cursor = cnx.cursor(buffered=True)

    # Executing query, storing answer in 'buff'
    get_query = ("SELECT * FROM bot_status")
    cursor.execute(get_query)

    # Going through status and start/stop appropriate bots
    settings = cursor
    for data in settings:
        if data[2] != data[6]:
            if data[2] == 1 and data[6] == 0:
                start(data[0], "like")
                update_db("like_a", 1, data[0])

            elif data[2] == 0 and data[6] == 1:
                stop(data[0], "like")
                update_db("like_a", 0, data[0])

    # Closing connection
    cursor.close()
    cnx.close()
