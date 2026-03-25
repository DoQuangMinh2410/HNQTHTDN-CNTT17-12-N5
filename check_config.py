
import requests
import json
import os

print("--- START DEBUG ---")
try:
    # get_param needs sudo() if not in superuser context
    api_key = env['ir.config_parameter'].sudo().get_param('nhan_su.gemini_api_key')
    print(f"API Key retrieved from DB: '{api_key}'")

    if not api_key:
        print("ERROR: API Key is empty!")
    else:
        # Test connectivity
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": "Say hi back"}]}]}
        
        print(f"Testing connectivity to: {url[:60]}...")
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
        print(f"HTTP Status: {response.status_code}")
        print(f"Response Body: {response.text}")

except Exception as e:
    print(f"UNEXPECTED ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

print("--- END DEBUG ---")
