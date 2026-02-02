import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rcon.source import Client

app = Flask(__name__)
CORS(app)

# --- LOCKED CREDENTIALS (CONFIRMED WORKING) ---
# We use 11690 because we proved it finds players and returns data.
ARK_IP = '31.214.239.14'
ARK_PORT = 11690
ARK_PASS = '3uKmTEuM'

print("-------------------------------------------------")
print(f"✅ SYSTEM LOCKED. TARGET: {ARK_IP}:{ARK_PORT}")
print("-------------------------------------------------")

def run_rcon(command):
    try:
        # Timeout 15s to prevent hanging
        with Client(ARK_IP, ARK_PORT, passwd=ARK_PASS, timeout=15) as client:
            print(f"🚀 SENDING: {command}")
            response = client.run(command)
            
            # ARK often returns an empty string for success
            if not response:
                return "✅ Executed"
            
            # Common success message from ARK
            if "Server received, But no response" in response:
                return "✅ Success"
            
            return response
            
    except Exception as e:
        error = str(e)
        print(f"❌ RCON ERROR: {error}")
        
        if "Connection refused" in error:
            return "❌ CONNECTION REFUSED. Server might be restarting."
        if "timed out" in error:
            return "❌ TIMED OUT. Check if server is online."
        if "Authentication failed" in error:
            return "❌ WRONG PASSWORD."
            
        return f"❌ Error: {error}"

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
