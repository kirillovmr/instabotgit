from subprocess import call
from sys import platform
from my_func import *
import misc
import os

python = misc.python_version()

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

start_manager_command = "{} {}/manager.py".format(python, path_)

while True:
    manager = call(start_manager_command, shell=True)
    print(restart_text)
    time.sleep(20)
