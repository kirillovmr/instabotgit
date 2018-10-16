from sys import platform # mac or linux
import huepy # for color print

path = {
    'darwin': '/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/instabot',
    'linux': '/usr/local/lib/python3.5/dist-packages/instabot',
    'win32': 'c:\\users\\user\\appdata\\local\\programs\\python\\python37\\lib\\site-packages\\instabot'
}

scriptName = {
    'hashtag_users': 'Кто выложил фото по хештегу',
    'check_vip': 'Проверка подписки на випов',
    'check_tags': 'Проверка папки "Фото со мной"',
    'check_hashtags': 'Проверка лайков по хештегу'
}

login = "_friendly_company"
password = "arina4ever699516"
# proxy = "http://oxanaroma:A0z2CkV@31.41.219.235:65233"
proxy = ""
post_link = "https://www.instagram.com/p/"
vip_filename = 'vip.txt'
check_users_filename = 'check_follows.txt'

hello = '''
    _________________________________________

      {}
    _________________________________________
'''

def getOs():
    return platform.lower()

def getPath():
    try:
        return path[getOs()]
    except KeyError:
        return None

def console_print(text, color=None):
    if color is not None:
        text = getattr(huepy, color)(text)
    print(text)
