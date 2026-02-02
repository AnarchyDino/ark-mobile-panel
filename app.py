import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rcon.source import Client

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
# ⚠️ IF YOU ARE STUCK, REPLACE THESE 'os.environ' LINES WITH YOUR ACTUAL NUMBERS ⚠️
# Example: ARK_IP = '85.190.123.45'
ARK_IP = os.environ.get('ARK_IP', '31.214.239.14')
ARK_PORT = int(os.environ.get('ARK_PORT', '11690'))
ARK_PASS = os.environ.get('ARK_PASS', '3uKmTEuM')

print("-------------------------------------------------")
print(f"✅ APP STARTING. TARGETING: {ARK_IP}:{ARK_PORT}")
print("-------------------------------------------------")

def run_rcon(command):
    try:
        # Connect to ARK
        with Client(ARK_IP, ARK_PORT, passwd=ARK_PASS, timeout=10) as client:
            print(f"🚀 SENDING: {command}")
            response = client.run(command)
            print(f"📥 RECEIVED: {response}")
            
            # Handle empty success messages from ARK
            if not response:
                return "✅ Executed (No return message)"
            if "Server received, But no response" in response:
                return "✅ Success"
            
            return response
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ ERROR: {error_msg}")
        
        # Friendly Error Translation
        if "Connection refused" in error_msg:
            return "❌ CONNECTION REFUSED. Check your IP and RCON PORT (Not Game Port)."
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
    response = run_rcon(cmd)
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
    # Debug print to Render Logs
    print(f"Command received: {cmd}")
    
    response = run_rcon(cmd)
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
