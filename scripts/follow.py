import time
i = 0
while True:
    print("FOLLOW {}".format(i))
    i += 1
    time.sleep(1)
    if i > 13:
        break
