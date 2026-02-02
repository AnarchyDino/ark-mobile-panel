import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rcon.source import Client

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION (Loaded from Cloud Environment Variables) ---
# We use environment variables so your passwords aren't visible in the code itself.
ARK_IP = os.environ.get('ARK_IP', '31.214.239.14')
ARK_PORT = int(os.environ.get('ARK_PORT', 11690))
ARK_PASS = os.environ.get('ARK_PASS', '3uKmTEuM')
WEB_ACCESS_CODE = os.environ.get('WEB_ACCESS_CODE', 'Taker420') # Password to use the website

def run_rcon(command):
    try:
        with Client(ARK_IP, ARK_PORT, passwd=ARK_PASS, timeout=5) as client:
            response = client.run(command)
            return response
    except Exception as e:
        return f"Connection Error: {e}"

@app.route('/')
def home():
    """Serves the actual website."""
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    
    # SECURITY CHECK
    user_code = data.get('access_code')
    if user_code != WEB_ACCESS_CODE:
        return jsonify({"response": "⛔ ACCESS DENIED: Incorrect Web Password"}), 403

    cmd = data.get('command')
    response = run_rcon(cmd)
    return jsonify({"response": response})

if __name__ == '__main__':
    # Render requires the app to listen on port 10000 or $PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
