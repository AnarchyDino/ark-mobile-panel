import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rcon.source import Client

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
ARK_IP = os.environ.get('ARK_IP', '31.214.239.14')
ARK_PORT = int(os.environ.get('ARK_PORT', 25000))
ARK_PASS = os.environ.get('ARK_PASS', '3uKmTEuM')

print(f"✅ SYSTEM ONLINE. TARGET: {ARK_IP}:{ARK_PORT}")

def run_rcon(command):
    try:
        # 15s timeout
        with Client(ARK_IP, ARK_PORT, passwd=ARK_PASS, timeout=15) as client:
            response = client.run(command)
            
            if not response:
                return "✅ Executed"
            if "Server received, But no response" in response:
                return "✅ Success"
            
            return response
            
    except Exception as e:
        error = str(e)
        print(f"❌ RCON ERROR: {error}")
        
        if "Connection refused" in error:
            return "❌ CONNECTION REFUSED. Check ARK_PORT."
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
