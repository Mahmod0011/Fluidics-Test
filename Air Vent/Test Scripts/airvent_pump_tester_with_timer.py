from datetime import datetime
import csv
import time
import threading

try:
    import serial
except ModuleNotFoundError:
    raise ImportError("Please install pyserial using 'pip install pyserial'")

# === CONFIGURATION ===
PUMP_PORT = "COM14"
ARDUINO_PORT = "COM10"
BAUD_RATE = 115200
CSV_FILENAME = f"air_bubble_experiment_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

# === Adjustable Experiment Steps ===
EXPERIMENT_STEPS = [
    {"label": "Pump ON (Baseline)", "duration": 40, "rpm": 200, "solenoid": False},
    {"label": "Pump + Air ON", "duration": 50, "rpm": 200, "solenoid": True},
    {"label": "Pump only (Mixed)", "duration": 90, "rpm": 200, "solenoid": False},
    {"label": "Pulsed Air (10 min)", "duration": 600, "rpm": 200, "solenoid": "pulsed"},  # 10s on/off loop
    {"label": "Pump only", "duration": 300, "rpm": 200, "solenoid": False},
    {"label": "Pump OFF", "duration": 600, "rpm": 0, "solenoid": False},
    {"label": "Pulsed Air (20 min)", "duration": 1200, "rpm": 200, "solenoid": "pulsed"},  # 10s on/off loop
    {"label": "Air only", "duration": 180, "rpm": 200, "solenoid": True},
    {"label": "Final Pump only", "duration": 240, "rpm": 200, "solenoid": False},
]

# === Shared State ===
current_rpm = 0
solenoid_state = False
air_bubble_status = "UNKNOWN"
stop_threads = False

# === Serial Setup ===
try:
    pump_ser = serial.Serial(PUMP_PORT, BAUD_RATE, timeout=1)
    print(f"✅ Pump connected on {PUMP_PORT}")
except Exception as e:
    raise SystemExit(f"❌ Pump connection failed: {e}")

try:
    arduino_ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    print(f"✅ Arduino connected on {ARDUINO_PORT}")
except Exception as e:
    pump_ser.close()
    raise SystemExit(f"❌ Arduino connection failed: {e}")

# === CSV Init ===
with open(CSV_FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Step", "RPM", "Solenoid", "AirBubble"])

# === Arduino Reader ===
def read_arduino():
    global air_bubble_status, stop_threads
    while not stop_threads:
        try:
            if arduino_ser.in_waiting:
                line = arduino_ser.readline().decode().strip()
                if "AirBubble:" in line:
                    parts = line.split("|")
                    for p in parts:
                        if "AirBubble:" in p:
                            air_bubble_status = p.split(":")[1].strip()
        except Exception as e:
            print(f"⚠️ Error reading from Arduino: {e}")
        time.sleep(0.1)

reader_thread = threading.Thread(target=read_arduino)
reader_thread.start()

# === Command Functions ===
def send_rpm(rpm):
    global current_rpm
    current_rpm = rpm
    pump_ser.write(f"{rpm}\n".encode())
    print(f"[PUMP] Set RPM to {rpm}")

def set_solenoid(state: bool):
    global solenoid_state
    solenoid_state = state
    arduino_ser.write(b"1\n" if state else b"0\n")
    print(f"[VALVE] Solenoid {'ON' if state else 'OFF'}")

def log_state(step_label):
    timestamp = datetime.now().isoformat()
    with open(CSV_FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, step_label, current_rpm, "ON" if solenoid_state else "OFF", air_bubble_status])
    return timestamp

# === Countdown Timer with Logging & Console Display ===
def run_step(step):
    label = step["label"]
    duration = step["duration"]
    rpm = step["rpm"]
    solenoid = step["solenoid"]

    print(f"\n➡️ Step: {label} ({duration}s)")
    send_rpm(rpm)

    if solenoid == "pulsed":
        cycle = 10
        end_time = time.time() + duration
        while time.time() < end_time:
            set_solenoid(True)
            for i in range(cycle):
                remaining = int(end_time - time.time())
                timestamp = log_state(label + " (Air ON)")
                if i % 2 == 0:
                    print(f"[{timestamp}] {label} | RPM={current_rpm} | Solenoid=ON | AirBubble={air_bubble_status} | {remaining}s left")
                time.sleep(1)
            set_solenoid(False)
            for i in range(cycle):
                remaining = int(end_time - time.time())
                timestamp = log_state(label + " (Air OFF)")
                if i % 2 == 0:
                    print(f"[{timestamp}] {label} | RPM={current_rpm} | Solenoid=OFF | AirBubble={air_bubble_status} | {remaining}s left")
                time.sleep(1)
    else:
        set_solenoid(solenoid)
        for sec in range(duration):
            timestamp = log_state(label)
            if sec % 2 == 0:
                remaining = duration - sec
                print(f"[{timestamp}] {label} | RPM={current_rpm} | Solenoid={'ON' if solenoid_state else 'OFF'} | AirBubble={air_bubble_status} | {remaining}s left")
            time.sleep(1)

# === Run Experiment ===
try:
    for step in EXPERIMENT_STEPS:
        run_step(step)

    print("\n✅ Experiment complete.")

except KeyboardInterrupt:
    print("\n🛑 Experiment interrupted by user.")

finally:
    stop_threads = True
    reader_thread.join()
    send_rpm(0)
    set_solenoid(False)
    pump_ser.close()
    arduino_ser.close()
    print(f"📁 Data saved to: {CSV_FILENAME}")
