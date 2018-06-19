import random
import time
a = [1,2,3,4,5,6,7]
random.shuffle(a)
posted = 0

while True:
    i = posted % len(a)
    print(i)
    time.sleep(1)
    posted += 1
