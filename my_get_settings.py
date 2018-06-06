import mysql.connector

HOST = 'belyy00.mysql.tools'
USER = 'belyy00_bot'
PASS = 'Kirillov44'
DB = 'belyy00_bot'

def get_settings(bot_id):
    # Connecting to DataBase
    cnx = mysql.connector.connect(host=HOST, user=USER, password=PASS, database=DB)
    cursor = cnx.cursor(buffered=True)

    # get_query = ("SELECT * FROM bot_settings WHERE bot_id={}".format(bot_id))
    get_query = ("SELECT * FROM `bot_settings`")
    cursor.execute(get_query)
    buff = cursor

    # Initializing settings dictionary
    settings = dict()

    # Filling settings dict with values from Database
    for data in buff:
        settings['login'] = data[1]
        settings['password'] = data[2]

    cursor.close()
    cnx.close()

    return settings
