import tkinter as tk
from tkinter import font
import requests
import threading

# --- CONFIGURATION ---
# Use the URL from your screenshot
FIREBASE_URL = 'https://biostream-150bf-default-rtdb.firebaseio.com/live_vitals.json'

class BioStreamMobileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BioStream Mobile")
        self.root.geometry("360x700") # Exact size of a generic Android phone
        self.root.configure(bg="#121212") # Dark Mobile Background
        self.root.resizable(False, False) # Fixed size like a phone

        # 1. App Bar / Header
        header = tk.Frame(root, bg="#1F1B24", height=60)
        header.pack(fill="x")
        # Title
        tk.Label(header, text="BioStream", font=("Roboto", 18, "bold"), bg="#1F1B24", fg="#00E5FF").place(x=20, y=15)
        # Connected Indicator
        tk.Label(header, text="● Live", font=("Arial", 10), bg="#1F1B24", fg="#00E676").place(x=300, y=20)

        # Scrollable-like Container for cards
        container = tk.Frame(root, bg="#121212")
        container.pack(fill="both", expand=True, padx=15, pady=20)

        # 2. Heart Rate Card (Red)
        self.create_card(container, "HEART RATE", "BPM", "#FF4081", "hr_val")

        # 3. SpO2 Card (Cyan)
        self.create_card(container, "BLOOD OXYGEN", "%", "#00E5FF", "spo2_val")

        # 4. Temp Card (Yellow)
        self.create_card(container, "TEMPERATURE", "°C", "#FFEB3B", "temp_val")

        # 5. Motion Card (Green)
        self.create_card(container, "BODY MOTION", "Accel", "#76FF03", "motion_val")

        # Status Bar at bottom
        self.status_bar = tk.Label(root, text="Syncing with Cloud...", font=("Arial", 9), bg="#121212", fg="gray")
        self.status_bar.pack(side=tk.BOTTOM, pady=10)

        # Start Data Loop
        self.update_data()

    def create_card(self, parent, title, unit, color, var_name):
        # Card Background
        card = tk.Frame(parent, bg="#1E1E1E", bd=0, highlightthickness=0)
        card.pack(fill="x", pady=8, ipady=5)
        
        # Color Strip on the left
        strip = tk.Frame(card, bg=color, width=5)
        strip.pack(side="left", fill="y")
        
        # Content Container
        content = tk.Frame(card, bg="#1E1E1E")
        content.pack(side="left", fill="both", expand=True, padx=10)
        
        # Title Label
        tk.Label(content, text=title, font=("Arial", 8, "bold"), bg="#1E1E1E", fg="#AAAAAA").pack(anchor="w", pady=(5,0))
        
        # The Value Label (Big Number)
        lbl = tk.Label(content, text="--", font=("Arial", 28, "bold"), bg="#1E1E1E", fg=color)
        lbl.pack(anchor="w")
        
        # Save reference to label so we can update it later
        setattr(self, var_name, lbl)
        
        # Unit Label
        tk.Label(content, text=unit, font=("Arial", 10), bg="#1E1E1E", fg="#666666").pack(anchor="w", pady=(0,5))

    def update_data(self):
        # Run network request in thread to keep UI smooth
        threading.Thread(target=self.fetch_firebase, daemon=True).start()
        # Schedule next check in 1000ms (1 second)
        self.root.after(1000, self.update_data)

    def fetch_firebase(self):
        try:
            response = requests.get(FIREBASE_URL, timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data:
                    self.update_ui(data)
        except:
            pass

    def update_ui(self, data):
        # Update Labels safely
        try:
            self.hr_val.config(text=str(data.get('hr', '--')))
            self.spo2_val.config(text=str(data.get('spo2', '--')))
            self.temp_val.config(text=str(data.get('temp', '--')))
            
            ax = data.get('ax', 0.0)
            ay = data.get('ay', 0.0)
            self.motion_val.config(text=f"X:{ax:.2f} | Y:{ay:.2f}")

            status = data.get('status', 'Unknown')
            self.status_bar.config(text=f"Device Status: {status}")
            
            if "Live" in status:
                self.status_bar.config(fg="#00E676")
            else:
                self.status_bar.config(fg="orange")
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = BioStreamMobileApp(root)
    root.mainloop()