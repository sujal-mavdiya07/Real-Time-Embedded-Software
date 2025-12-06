<img width="6854" height="706" alt="Untitled diagram-2025-12-05-163252" src="https://github.com/user-attachments/assets/54cd1a16-fa9c-45cd-9f19-b4e7a0462d86" />Smart Health Monitoring System (RTES)

A real-time IoT health monitoring solution built on the STM32 Nucleo platform using FreeRTOS. This system collects vital signs (Heart Rate, SpO2, Temperature, Motion) and transmits them to a cloud dashboard for remote patient monitoring.

# Features

Real-Time Vitals: Monitors Heart Rate, SpO2, Body Temperature, and Patient Movement simultaneously.

RTOS Architecture: Uses FreeRTOS on STM32 for deterministic task scheduling (Sensor Acquisition, Processing, Communication).

Cloud Integration: Pushes data to Firebase Realtime Database for global accessibility.

Cross-Platform Monitoring:

Web Dashboard: Responsive HTML/JS interface with live Plotly graphs.

Mobile App: Python-based desktop/mobile client for caregivers.

Anomaly Detection: Automated analysis script to flag Tachycardia or Fever events.

🛠️ Tech Stack

Hardware: STM32 Nucleo-F411RE, MAX30102 (HR/SpO2), MPU6050 (Gyro), LM35 (Temp).

Firmware: C, STM32 HAL, FreeRTOS.

Backend/Gateway: Python, Flask, PySerial.

Cloud: Google Firebase.

🚀 How to Run

Firmware: Flash the code in Firmware/ to the STM32 Nucleo using STM32CubeIDE.

Backend:

pip install -r requirements.txt
python app.py


Mobile App:
python mobile_app.py


Web Dashboard: Open http://localhost:5000 in your browser.

For detailed technical documentation, please refer to the Project Report.

Developed by 
Sujal Mavdiya
DA-IICT, Gandhinagar
