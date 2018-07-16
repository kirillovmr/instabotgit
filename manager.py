import my_database
import my_telegram
import my_func
import time

my_telegram.send_mess_tg(my_database.get_admin_tg(), "✅ Manager started on {}".format(my_func.platform()))

not_notify = my_database.fill_not_notify_array()

# Set all actual values to 0 in database.
my_database.set_actual_zero()

while True:

    # Get statuses from database and start/stop bots
    my_database.get_bots_status(not_notify=not_notify)

    # Check running scripts. If closed - trying to restart
    my_func.checkrun()

    # Print running scripts
    my_func.print_running_array()
    if len(not_notify):
        print("--/--/-- N notif: {}".format(not_notify))

    # Clears a feedback_required array if needed. Used to
    my_func.clear_feedback_required()

    time.sleep(30)
