import deepl
# Languages: https://www.deepl.com/en/docs-api/translating-text/#:~:text=Sets%20whether%20the%20translated%20text,%22RU%22%20(Russian).

# Variable initialization
key = ""
with open("deepL auth.txt", "r") as f:
    key = f.read()
translator = deepl.Translator(key)


if __name__ == "__main__":
    # Operation
    result = translator.translate_text("好", source_lang="ZH", target_lang="EN-US")
    print(result.text)