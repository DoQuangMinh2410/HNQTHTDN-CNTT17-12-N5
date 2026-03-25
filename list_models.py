import requests
import json

api_key = "AIzaSyCCmF3F9o1aRfdr2ToJlexJQNlbeI5wEzY"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json().get('models', [])
        print("Available Models:")
        for m in models:
            print(f"- {m['name']}")
    else:
        print(f"Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"Error: {e}")
