import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rcon.source import Client

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
ARK_IP = os.environ.get('ARK_IP', '31.214.239.14')
ARK_PORT = int(os.environ.get('ARK_PORT', 11690))
ARK_PASS = os.environ.get('ARK_PASS', '3uKmTEuM')

print(f"✅ SYSTEM ONLINE. TARGET: {ARK_IP}:{ARK_PORT}")

def run_rcon(command):
    try:
        # 15s timeout
        with Client(ARK_IP, ARK_PORT, passwd=ARK_PASS, timeout=15) as client:
            response = client.run(command)
            
            # Weather commands return NOTHING when successful. 
            # We must catch this empty string or the app thinks it failed.
            if not response:
                return "✅ Executed"
            if "Server received, But no response" in response:
                return "✅ Success"
            
            return response
            
    except Exception as e:
        error = str(e)
        print(f"❌ RCON ERROR: {error}")
        
        if "Connection refused" in error:
            return "❌ CONNECTION REFUSED. Check IP and ensure ARK_PORT is the RCON Port (e.g. 27020)."
        if "Authentication failed" in error:
            return "❌ WRONG PASSWORD."
        if "timed out" in error:
            return "❌ TIMED OUT. Server offline?"
            
        return f"❌ Error: {error}"

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
    
    # Run the command
    response = run_rcon(cmd)
    
    # THIS LINE MUST BE INDENTED (4 SPACES)
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
