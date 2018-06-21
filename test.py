from my_database import *
from my_func import *
from datetime import datetime

from instabot import Bot
bot = Bot()

check_delay = 60*60

db = db_connect()

while True:
    # SELECT BOT_ID and FOLLOW_LIMIT only for running bots
    get_follow_q = ("SELECT `bots`.`bot_id`,`bots`.`login`,`bots`.`password`,`bots`.`proxy`,`bots`.`follow_delay`,`bots`.`follow_limit` FROM `bots`,`bot_status` WHERE `bots`.`bot_id` = `bot_status`.`bot_id` AND `bot_status`.`follow_s` = 1")
    db['cursor'].execute(get_follow_q)
    buff = db['cursor']

    for bot_row in buff:
        id = bot_row[0]
        login = bot_row[1]
        password = bot_row[2]
        proxy = bot_row[3]
        follow_delay = bot_row[4]
        follow_limit = bot_row[5]

        # Going to current bot folder
        os.chdir("{}/instabot/accs/{}".format(path_, id))

        bot.login(username=login, password=password,
                  proxy=proxy)

        # Getting following count
        user_id = bot.convert_to_user_id(login)
        user_info = bot.get_user_info(user_id)
        following_count = user_info["following_count"]

        print("id:{} | now:{} | limit:{}".format(id, following_count, follow_limit))

        ##### Checking
        # zapas - number of follows that can be done before next check
        zapas = int((check_delay/follow_delay) + 2) # + 2 follows for safe

        if following_count + zapas >= follow_limit:
            print("Bot {} reached follow limit. Going to unfollow".format(id))

    print("{} Waiting {}s. before next check.".format(now_time(), check_delay))
    time.sleep(check_delay)
