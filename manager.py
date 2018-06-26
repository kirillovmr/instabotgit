import my_database
import my_func
import time

# Set all actual values to 0 in database.
my_database.set_actual_zero()

while True:
    # Check if need to stop follow / unfollow


    # Get statuses from database and start/stop bots
    my_database.get_bots_status()

    # Check running scripts. If closed - trying to restart
    my_func.checkrun()

    # Print running scripts
    my_func.print_running_array()

    time.sleep(30)
