from my_database import *
from my_func import *

# Set all actual values to 0 in database.
set_actual_zero()

# time.sleep(100)

while True:

    # Get statuses from database and start/stop bots
    get_bots_status()

    # Check running scripts. If closed - trying to restart
    checkrun()

    # Print running scripts
    print_running_array()

    time.sleep(20)
