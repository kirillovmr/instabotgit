import my_database
import my_func
import time

# Set all actual values to 0 in database.
my_database.set_actual_zero()

while True:

    # Get statuses from database and start/stop bots
    my_database.get_bots_status()

    # Check running scripts. If closed - trying to restart
    my_func.checkrun()

    # Print running scripts
    my_func.print_running_array()

    # Clears a feedback_required array if needed. Used to
    my_func.clear_feedback_required()

    time.sleep(30)
