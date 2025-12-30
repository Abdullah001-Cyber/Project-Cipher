from flask import Flask, request, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# --- CONFIGURATION ---
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

BLOCKED_AGENTS = ["curl", "python-requests", "scrapy", "bot", "crawler", "spider"]

# --- HTML TEMPLATES ---
HOME_HTML = """
<!DOCTYPE html>
<html>
<body>
    <h1>Welcome to the Secure Server</h1>
    <form action="/process_login" method="POST">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <input type="text" name="trap_field" style="display:none;" autocomplete="off">
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

ACCESS_DENIED_HTML = """
<!DOCTYPE html>
<html>
<body style="background-color:black; color:red; text-align:center; padding-top:50px;">
    <h1>ACCESS DENIED</h1>
    <p>Reason: {{ reason }}</p>
</body>
</html>
"""

# --- LOGIC ---
def is_bot(request):
    user_agent = request.headers.get('User-Agent', '').lower()
    print(f"DEBUG: Incoming User-Agent is: {user_agent}") # PRINT USER AGENT

    if not user_agent:
        return True, "No User-Agent provided"
        
    for bot_name in BLOCKED_AGENTS:
        if bot_name in user_agent:
            print(f"DEBUG: Found blocked keyword: {bot_name}")
            return True, f"Blocked User-Agent detected: {bot_name}"
            
    return False, "Clean"

# --- ROUTES ---
@app.route('/')
def home():
    bot_detected, reason = is_bot(request)
    if bot_detected:
        return render_template_string(ACCESS_DENIED_HTML, reason=reason), 403
    return render_template_string(HOME_HTML)

@app.route('/process_login', methods=['POST'])
def process_login():
    print("--- NEW LOGIN ATTEMPT ---")
    
    # 1. Print what the user sent
    form_data = request.form
    print(f"DEBUG: Form Data Received: {form_data}")
    
    # 2. Check the Honeypot
    honeypot_value = request.form.get('trap_field')
    print(f"DEBUG: Honeypot Value: '{honeypot_value}'")
    
    if honeypot_value:
        print(">>> DETECTION: Honeypot was filled! BLOCKING.")
        return render_template_string(ACCESS_DENIED_HTML, reason="Honeypot Triggered"), 403
    
    print(">>> PASS: Honeypot was empty. Allowing user.")
    return "<h1>Welcome, Human!</h1>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)