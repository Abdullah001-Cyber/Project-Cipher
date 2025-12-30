import requests

# 1. We lie and say we are a real browser (Chrome)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 2. BUT, we dumbly fill out the 'trap_field'
data = {
    'username': 'hacker',
    'password': 'password123',
    'trap_field': 'I AM A BOT'  # <--- This triggers the trap
}

print("Attempting to hack the server...")

try:
    response = requests.post('http://127.0.0.1:5000/process_login', data=data, headers=headers)
    
    print(f"Server responded with Code: {response.status_code}")
    
    if response.status_code == 403:
        print("SUCCESS: The Bot Detector blocked us!")
        print("Server Message:", response.text)
    else:
        print("FAILURE: The Bot Detector missed us.")

except Exception as e:
    print("Error:", e)