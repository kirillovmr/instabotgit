import logging
import socket
import sys

from subprocess import call
import my_func
import time

lock_socket = None  # we want to keep the socket open until the very end of
                    # our script so we use a global variable to avoid going
                    # out of scope and being garbage-collected

def is_lock_free():
    global lock_socket
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_id = "kirillovmr.manager_control"   # this should be unique. using your username as a prefix is a convention
        lock_socket.bind('\0' + lock_id)
        logging.debug("Acquired lock %r" % (lock_id,))
        return True
    except socket.error:
        # socket already locked, task must already be running
        logging.info("Failed to acquire lock %r" % (lock_id,))
        return False

if not is_lock_free():
    sys.exit()

# then, either include the rest of your script below,
# or import it, if it's in a separate file:
print(my_func.mc_start_text)

start_manager_command = "{} {}/manager.py".format(my_func.python_version(), my_func.path())

while True:
    manager = call(start_manager_command, shell=True)
    print(my_func.mc_restart_text)
    time.sleep(10)
