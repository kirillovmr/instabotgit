import my_telegram
import my_database
import json

inline_button1 = { "text": 'Stop THIS bot', "callback_data": '/stop mrkirillov like' }
inline_keyboard = [[inline_button1]]
keyboard = { "inline_keyboard": inline_keyboard }
markup = json.JSONEncoder().encode(keyboard)

my_telegram.send_mess_tg(my_database.get_chat_ids_tg(2), "Bot test", replyMarkup=markup)
