import json

with open("rozvrhy.json", "r") as json_data:
    rozvrhy = json.load(json_data)
    mimo_rozvrh = False

def in_time(range, cas):
    print(range, cas)
    pred = (range[0][0] > cas[0]) or ((range[0][0] == cas[0]) and (range[0][1] > cas[1]))
    po =   (range[1][0] < cas[0]) or ((range[1][0] == cas[0]) and (range[1][1] < cas[1]))
    return not (pred or po)

def break_time(cas, rozvrhy):
    for prestavka in rozvrhy["prestavky"]:
        if in_time(rozvrhy["prestavky"][prestavka], cas):
            return prestavka
    return False


print(break_time((12,25), rozvrhy))
