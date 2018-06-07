import os
import sys
import time

a = " top_kherson vip_kherson kherson   "
b = a.strip()

array = []
while b.find(" ") >= 0:
    pos = b.find(" ")
    array.append(b[:pos])
    b = b[pos+1:]
array.append(b)

print(array)
