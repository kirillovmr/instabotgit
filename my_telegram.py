import requests

token = "582921490:AAGWjO2-ui756y1IB8Sa0ZnlkupVCp79u5w"
url = "https://api.telegram.org/bot{}/".format(token)

def send_mess_tg(chats, text, replyMarkup = None):
    for chat in chats:

        params = {'chat_id': chat, 'text': text, 'reply_markup': replyMarkup}
        response = requests.post(url + 'sendMessage', data=params)
        return response
