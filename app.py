import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rcon.source import Client

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
# We still need these to talk to the ARK Server
ARK_IP = os.environ.get('ARK_IP', '31.214.239.14')
ARK_PORT = int(os.environ.get('ARK_PORT', 11690))
ARK_PASS = os.environ.get('ARK_PASS', '3uKmTEuM')

def run_rcon(command):
    try:
        # 15s timeout for stability
        with Client(ARK_IP, ARK_PORT, passwd=ARK_PASS, timeout=15) as client:
            response = client.run(command)
            
            if not response:
                return "✅ Executed"
            if "Server received, But no response" in response:
                return "✅ Success"
            
            return response
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    cmd = data.get('command')
    
    # Debug print to Render Logs
    print(f"Command received: {cmd}")
    
    response = run_rcon(cmd)
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    
    # 1. Check Website Password
    if data.get('access_code') != WEB_ACCESS_CODE:
        return jsonify({"response": "⛔ WRONG WEBSITE ACCESS CODE"}), 403

    # 2. Run the Command
    cmd = data.get('command')
    print(f"Executing: {cmd}") # Print to Render logs for debugging
    response = run_rcon(cmd)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    # Render assigns the PORT environment variable automatically
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
def send_command():
    data = request.json
    
    # SECURITY CHECK
    if data.get('access_code') != WEB_ACCESS_CODE:
        return jsonify({"response": "⛔ WRONG PASSWORD"}), 403

    cmd = data.get('command')
    response = run_rcon(cmd)
    
    # This return MUST be indented so it is inside the function
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
