"""
    Bot - Infinity hashtags liker.
"""
import os
import sys
import time
import random
import argparse
from sys import platform # mac or linux

from tqdm import tqdm

if "darwin" in platform.lower():
    print("Script launched on MAC OS")
    path_ = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/instabot"
elif "linux" in platform.lower():
    print("Script launched on LINUX")
    path_ = "/usr/local/lib/python3.4/dist-packages/instabot"
elif "win32" in platform.lower():
    print("Script launched on WINDOWS")
    path_ = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\instabot"
else:
    print("This platform is not supported. Exiting...")
    exit()

# sys.path.append(os.path.join(sys.path[0], '../'))
sys.path.append(path_)
from instabot import Bot

bot = Bot()
bot.login(username='rich_kherson', password='khKirillov44')

print(bot.get_user_info('rich_kherson'))
