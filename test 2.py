import json

data = {"showWelcomePage": True}

with open("Assets/data.json", "w") as f:
    json.dump(data, f)


with open("Assets/data.json", "r") as f:
    readData = json.load(f)

print(readData)