# utils.py

import os

def set_openai_api_key(api_key):
    os.environ["OPENAI_API_KEY"] = api_key
def print_response(response):
    print("Generated Response:", response['result'])
    print("Source Documents:")
    for doc in response['source_documents']:
        print(doc.page_content) 