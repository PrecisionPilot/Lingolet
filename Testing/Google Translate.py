import os
from google.cloud import translate_v2 as translate

# Authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Assets/google auth.json'

client = translate.Client()
# result = client.translate(values="ok then", target_language="ja")["translatedText"]

print(client.detect_language("是")["language"])

# output = client.translate(contents="ok then", target_language_code="ZH-CN")