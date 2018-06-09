import time
i = 0
while True:
    print("LIKE {}".format(i))
    i += 1
    time.sleep(1)
    if i > 10:
        break
