import json

# Map languages to their respective country codesf from json file
with open("Assets/DeepL translate codes.json") as f:
    deeplCodes = json.load(f)
with open("Assets/Google translate codes.json") as f:
    googleCodes = json.load(f)


for codeItem, languageItem in googleCodes.items():
    pass