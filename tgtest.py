import my_telegram
import my_database

my_telegram.send_mess_tg(my_database.get_chat_ids_tg(2), "Bot test")
