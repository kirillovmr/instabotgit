start_text = '''
##################################################

########    MANAGER CONTROLLER STARTED    ########

##################################################
'''
restart_text = '''
##################################################
####    manager was closed. restarting....    ####
##################################################
'''
print(start_text)

from subprocess import call
from my_func import *

start_manager_command = "python3 {}/instabot/manager.py".format(path_)

while True:
    manager = call(start_manager_command, shell=True)
    print(restart_text)
    time.sleep(20)
