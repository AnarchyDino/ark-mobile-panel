import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rcon.source import Client

app = Flask(__name__)
CORS(app)

# --- HARDCODED CREDENTIALS ---
ARK_IP = '31.214.239.14'
ARK_PASS = '3uKmTEuM'

# We will try ALL of these ports to find the real one
POSSIBLE_PORTS = [11690, 11691, 11692, 27015, 27020]

print("-------------------------------------------------")
print(f"✅ SYSTEM BOOT. SCANNING PORTS: {POSSIBLE_PORTS}")
print("-------------------------------------------------")

def run_rcon(command):
    # Try every port in the list until one works
    for port in POSSIBLE_PORTS:
        try:
            print(f"🔍 TRYING PORT: {port}...")
            with Client(ARK_IP, port, passwd=ARK_PASS, timeout=5) as client:
                response = client.run(command)
                
                # If we get here, we connected!
                print(f"✅ CONNECTED ON PORT {port}!")
                print(f"📥 RECEIVED: {response}")
                
                # If ListPlayers returns "No response", it's a Ghost Port -> Ignore it
                if command == "ListPlayers" and "Server received, But no response" in response:
                    print(f"⚠️ PORT {port} IS A GHOST (Game Port). IGNORING.")
                    continue 

                if not response:
                    return f"✅ Executed (via Port {port})"
                if "Server received, But no response" in response:
                    return f"✅ Success (via Port {port})"
                
                return f"{response} (via Port {port})"
                
        except Exception as e:
            print(f"❌ PORT {port} FAILED: {e}")
            continue # Try the next port
            
    return "❌ FAILED: All ports refused connection."

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
