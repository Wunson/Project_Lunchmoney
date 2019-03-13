from time import localtime, time
import json

def what_day(num):
    days = ("po", "ut", "st", "ct", "pa", "so", "ne")
    return days[num]

cas = localtime(time())
day = what_day(cas.tm_wday)
cas = (cas.tm_hour,cas.tm_min)
print(cas, day)

with open("rozvrhy.json", "r") as json_data:
    rozvrhy = json.load(json_data)


    print(rozvrhy["prestavky"]["2"])
