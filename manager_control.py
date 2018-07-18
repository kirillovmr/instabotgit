from subprocess import call
import my_func
import time

print(my_func.mc_start_text)

# my_func.gitfetch(my_func.path())

start_manager_command = "{} {}/manager.py".format(my_func.python_version(), my_func.path())

while True:
    manager = call(start_manager_command, shell=True)
    print(my_func.mc_restart_text)
    time.sleep(10)
