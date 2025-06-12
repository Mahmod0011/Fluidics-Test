# Air Bubble Detection Pump Control Script

This Python script automates an 9-phase liquid flow experiment involving a **pump** and a **solenoid-controlled air injection valve**, while logging air bubble detection status from an Arduino-connected SENSIRION flow sensor.

---

## Features

- Controls pump RPMs via serial (COM port)
- Opens/closes solenoid air valve to introduce air into the system
- Logs experiment progress every second
- Prints status to terminal every 2 seconds
- Logs all activity to a CSV file with timestamps
- Detects air bubbles via serial input from an Arduino


---

## CSV Output Format

Each row in the CSV file contains:

| Timestamp           | Step                | RPM | Solenoid | AirBubble |
|---------------------|---------------------|-----|----------|-----------|
| ISO 8601 timestamp  | Current step name   | int | ON/OFF   | YES/NO    |

---

## Requirements

- Python 3.x
- [PySerial](https://pypi.org/project/pyserial/)

Install with:

```bash
pip install pyserial
