import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import firebase_admin
from firebase_admin import credentials, db

# --- CONFIGURATION ---
# Set this to TRUE if you have real history in Firebase you want to analyze.
# Set to FALSE to generate a realistic "Demo Day" dataset.
USE_REAL_FIREBASE_DATA = False 

def fetch_mock_data():
    """Generates a realistic 24-hour dataset for demonstration."""
    print("--- GENERATING DEMO PATIENT DATA (24 Hours) ---")
    periods = 1440 # Minutes in a day
    
    # Base baselines
    time_index = pd.date_range(start='2025-12-04 00:00:00', periods=periods, freq='T')
    
    # 1. Heart Rate: Sleep (60s) -> Morning (70s) -> Workout Spike (130s) -> Normal
    hr = np.random.normal(70, 5, periods)
    hr[400:460] += 50 # Morning Jog Spike (High HR)
    hr[0:360] -= 10   # Sleeping (Low HR)

    # 2. Temperature: Normal fluctuation + Fever Spike in evening
    temp = np.random.normal(36.6, 0.1, periods)
    temp[1000:1200] += 1.5 # Fever event

    # 3. SpO2: Mostly stable, occasional drops
    spo2 = np.random.normal(98, 0.5, periods)
    spo2 = np.clip(spo2, 90, 100) # Keep within realistic bounds

    # Create DataFrame
    df = pd.DataFrame({'Time': time_index, 'HeartRate': hr, 'Temp': temp, 'SpO2': spo2})
    return df

def fetch_firebase_data():
    """Fetches real recorded data from your Firebase Cloud."""
    print("--- FETCHING REAL DATA FROM FIREBASE ---")
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://biostream-150bf-default-rtdb.firebaseio.com/'})
        
        # Fetch the 'history' node (Requires you to have pushed data to 'history' in app.py)
        ref = db.reference('history') 
        data = ref.get()
        
        if data:
            # Convert JSON to DataFrame
            df = pd.DataFrame.from_dict(data, orient='index')
            # Convert timestamp to datetime
            df['Time'] = pd.to_datetime(df['timestamp'], unit='s')
            return df
        else:
            print("No history found in Firebase. Switching to Mock Data.")
            return fetch_mock_data()
    except Exception as e:
        print(f"Error connecting to Firebase: {e}")
        return fetch_mock_data()

# --- MAIN ANALYSIS ---

# 1. Get Data
if USE_REAL_FIREBASE_DATA:
    df = fetch_firebase_data()
else:
    df = fetch_mock_data()

# 2. Statistical Analysis
avg_hr = df['HeartRate'].mean()
max_hr = df['HeartRate'].max()
min_spo2 = df['SpO2'].min()
avg_temp = df['Temp'].mean()
max_temp = df['Temp'].max()

# 3. Generate Text Report
print("\n" + "="*40)
print("       BIOSTREAM HEALTH REPORT       ")
print("="*40)
print(f"Observation Period: {len(df)} minutes")
print("-" * 30)
print(f"Heart Rate (Avg):   {avg_hr:.1f} BPM")
print(f"Heart Rate (Max):   {max_hr:.1f} BPM")
print(f"Body Temp (Avg):    {avg_temp:.1f} °C")
print(f"Body Temp (Max):    {max_temp:.1f} °C")
print(f"Lowest SpO2:        {min_spo2:.1f} %")
print("-" * 30)

print("ANOMALY DETECTION:")
anomalies = 0
if max_hr > 100:
    print(f"[!] TACHYCARDIA ALERT: HR spiked to {max_hr:.0f} BPM during exercise/stress.")
    anomalies += 1
if max_temp > 37.5:
    print(f"[!] FEVER ALERT: Temperature reached {max_temp:.1f}°C. Potential infection.")
    anomalies += 1
if min_spo2 < 95:
    print(f"[!] HYPOXIA WARNING: Oxygen levels dropped to {min_spo2:.1f}%.")
    anomalies += 1

if anomalies == 0:
    print("No significant anomalies detected. Patient is healthy.")
print("="*40)

# 4. Generate Professional Visualizations
plt.style.use('dark_background') # Matches your app theme
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Plot 1: Heart Rate
ax1.plot(df['Time'], df['HeartRate'], color='#ff4081', linewidth=1.5)
ax1.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='Tachycardia Threshold (100)')
ax1.set_title('Heart Rate Analysis', fontsize=14, color='white')
ax1.set_ylabel('BPM')
ax1.legend(loc='upper right')
ax1.grid(color='#333333')

# Plot 2: Temperature
ax2.plot(df['Time'], df['Temp'], color='#ffeb3b', linewidth=1.5)
ax2.axhline(y=37.5, color='orange', linestyle='--', alpha=0.7, label='Fever Threshold (37.5°C)')
ax2.set_title('Body Temperature Trends', fontsize=14, color='white')
ax2.set_ylabel('Celsius')
ax2.legend(loc='upper right')
ax2.grid(color='#333333')

# Plot 3: SpO2
ax3.plot(df['Time'], df['SpO2'], color='#00e5ff', linewidth=1.5)
ax3.axhline(y=95, color='cyan', linestyle='--', alpha=0.7, label='Hypoxia Threshold (95%)')
ax3.set_title('Oxygen Saturation (SpO2)', fontsize=14, color='white')
ax3.set_ylabel('Percent (%)')
ax3.set_xlabel('Time of Day')
ax3.legend(loc='lower right')
ax3.grid(color='#333333')

plt.tight_layout()
plt.show()