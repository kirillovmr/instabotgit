running = dict()
running[1] = []
running[1].append("comment")
running[1].append("like")
running[2] = []
running[2].append("1")
running[2].remove("1")
running[4] = []

# print(running)

# print(len(running[1]))

a = 143

# Return last digit
def lastdigit(int_):
    return int(str(int_)[len(str(int_))-1])

# Return number without last digit
def removelastdigit(int_):
    return int(int_ / 10)

# Return num of script
def scripttonum(script):
    if script == "follow":
        return 1
    elif script == "unfollow":
        return 2
    elif script == "like":
        return 3
    elif script == "comment":
        return 4
    elif script == "direct":
        return 5
    else:
        print("ERROR! scripttpnum() func cant parse {} param.".format(script))

# Return script name
def numtoscript(int_):
    if int_ == 1:
        return "follow"
    elif int_ == 2:
        return "unfollow"
    elif int_ == 3:
        return "like"
    elif int_ == 4:
        return "comment"
    elif int_ == 5:
        return "direct"
    else:
        print("ERROR! numtoscript() func cant parse '{}' param.".format(int_))

print("Original: {} | Separated: {} | Last: {}.".format(a, removelastdigit(a), lastdigit(a)))
print("Original: {} | Separated: {} | Script: {}.".format(a, removelastdigit(a), numtoscript(lastdigit(a))))
