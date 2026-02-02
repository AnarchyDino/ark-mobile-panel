import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rcon.source import Client

app = Flask(__name__)
CORS(app)

# --- HARDCODED CREDENTIALS (FROM NITRADO DASHBOARD) ---
# We use the Dashboard Port (11690), NOT the internal file port (25000).
ARK_IP = '31.214.239.14'
ARK_PORT = 11690
ARK_PASS = '3uKmTEuM'

print("-------------------------------------------------")
print(f"✅ SYSTEM BOOT. TARGETING: {ARK_IP}:{ARK_PORT}")
print("-------------------------------------------------")

def run_rcon(command):
    try:
        # Timeout 15s
        with Client(ARK_IP, ARK_PORT, passwd=ARK_PASS, timeout=15) as client:
            print(f"🚀 SENDING: {command}")
            response = client.run(command)
            
            if not response:
                return "✅ Executed"
            if "Server received, But no response" in response:
                return "✅ Success"
            
            return response
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ RCON ERROR: {error_msg}")
        
        if "Connection refused" in error_msg:
            return f"❌ CONNECTION REFUSED. Port {ARK_PORT} might be blocked or Server is restarting."
        if "timed out" in error_msg:
            return "❌ TIMED OUT. Server offline or IP wrong."
        if "Authentication failed" in error_msg:
            return "❌ WRONG PASSWORD."
            
        return f"❌ Error: {error_msg}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return "OK", 200

@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    cmd = data.get('command')
    response = run_rcon(cmd)
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
