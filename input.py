import json

while 1:
    inpu = input(">>")
    with open("input.json", "w") as json_data:
        json.dump(inpu, json_data)
