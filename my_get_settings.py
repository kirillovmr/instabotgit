import mysql.connector

HOST = 'belyy00.mysql.tools'
USER = 'belyy00_bot'
PASS = 'Kirillov44'
DB = 'belyy00_bot'

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
        settings['max_likes_per_day'] = data[4].strip()
        settings['max_follows_per_day'] = data[5].strip()
        settings['max_unfollows_per_day'] = data[6].strip()
        settings['max_comments_per_day'] = data[7].strip()
        settings['like_delay'] = data[8].strip()
        settings['follow_delay'] = data[9].strip()
        settings['unfollow_delay'] = data[10].strip()
        settings['comment_delay'] = data[11].strip()
        settings['message_delay'] = data[12].strip()
        settings['check_new_followers_delay'] = data[13].strip()
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
