import serial
import time
import threading
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, render_template
from flask_socketio import SocketIO

# --- FIREBASE SETUP ---
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://biostream-150bf-default-rtdb.firebaseio.com/' 
    })
    ref = db.reference('live_vitals')
    print("--- FIREBASE CONNECTED ---")
    firebase_active = True
except Exception as e:
    print(f"--- FIREBASE ERROR: {e}")
    firebase_active = False

# --- FLASK SETUP ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
SERIAL_PORT = 'COM5'
BAUD_RATE = 115200

current_data = {'hr': 0, 'temp': 0, 'spo2': 0, 'ax': 0, 'ay': 0, 'az': 0, 'status': 'Conn...'}

def read_serial():
    print(f"--- LISTENING ON {SERIAL_PORT} ---")
    while True:
        try:
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
                print("--- SERIAL CONNECTED ---")
                ser.reset_input_buffer()
                while True:
                    if ser.in_waiting > 0:
                        try:
                            raw = ser.readline().decode('utf-8', errors='ignore').strip()
                            parts = raw.split(',')
                            
                            # Expecting 7 parts now
                            if len(parts) >= 7:
                                current_data['hr'] = int(parts[0])
                                current_data['temp'] = float(parts[1])
                                current_data['spo2'] = int(parts[2])
                                current_data['ax'] = float(parts[3])
                                current_data['ay'] = float(parts[4])
                                current_data['az'] = float(parts[5])
                                current_data['status'] = parts[6]

                                # Print Full Data
                                print(f"[STM32] HR:{parts[0]} | SpO2:{parts[2]}% | T:{parts[1]}C | Motion:({parts[3]}, {parts[4]}, {parts[5]}) | {parts[6]}")

                                # Send to Local Dashboard
                                socketio.emit('update_data', current_data)

                                # Push to Firebase
                                if firebase_active:
                                    ref.set(current_data)
                        except Exception:
                            pass
                    time.sleep(0.05)
        except Exception:
            time.sleep(3)

thread = threading.Thread(target=read_serial)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, port=5500)