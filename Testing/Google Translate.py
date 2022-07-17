import os
from google.cloud import translate

# Authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Assets/google auth.json'

client = translate.TranslationServiceClient()

print(client.translate_text(contents="ok then", target_language_code="ja"))

# output = client.translate_text(contents="ok then", target_language_code="ZH-CN")