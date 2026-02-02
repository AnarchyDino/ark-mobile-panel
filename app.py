import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rcon.source import Client

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
# Falls back to 127.0.0.1 if not set in Render
ARK_IP = os.environ.get('ARK_IP', '31.214.239.14')
ARK_PORT = int(os.environ.get('ARK_PORT', 25000))
ARK_PASS = os.environ.get('ARK_PASS', '3uKmTEuM')

print("-------------------------------------------------")
print(f"✅ SYSTEM STARTING. TARGETING: {ARK_IP}:{ARK_PORT}")
print("-------------------------------------------------")

def run_rcon(command):
    try:
        # 15s timeout to allow for connection lag
        with Client(ARK_IP, ARK_PORT, passwd=ARK_PASS, timeout=15) as client:
            print(f"🚀 SENDING: {command}")
            response = client.run(command)
            print(f"📥 RECEIVED: {response}")
            
            # ARK often sends an empty string for success
            if not response:
                return "✅ Executed (No return message)"
            
            # ARK often sends this specific "error" string for success
            if "Server received, But no response" in response:
                return "✅ Success"
            
            return response
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ ERROR: {error_msg}")
        
        # Friendly Error Translation for the User
        if "Connection refused" in error_msg:
            return "❌ CONNECTION REFUSED. You are likely using the Game Port (7777). Change ARK_PORT to your RCON Port (e.g. 27020) in Render."
        if "timed out" in error_msg:
            return "❌ TIMED OUT. Server might be offline or IP is wrong."
        if "Authentication failed" in error_msg:
            return "❌ WRONG PASSWORD. Check ARK_PASS in Render."
            
        return f"❌ Error: {error_msg}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    cmd = data.get('command')
    
    # Run the RCON command
    response = run_rcon(cmd)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    # Render assigns the PORT automatically
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
