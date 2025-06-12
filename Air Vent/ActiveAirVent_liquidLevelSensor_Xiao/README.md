# Active Air Vent & Liquid Level Sensor – XIAO RA4M1

## Overview

This repository contains an Arduino sketch designed for contorl an **active air vent** using a **liquid level sensor** and a **solenoid valve**, controlled by the **Seeed Studio XIAO RA4M1** microcontroller. The system continuously monitors the liquid level and opens or closes the vent based on configurable thresholds to maintain optimal conditions.

## Features

- Monitors liquid level through an analog sensor.
- Controls an air vent via a solenoid valve.
- Uses threshold-based logic to trigger venting actions.
- Outputs live data and system state via serial communication.

## Hardware Requirements

- Seeed Studio **XIAO RA4M1**
- **Analog liquid level sensor**
- **Solenoid valve** (with driver circuit)

## Pin Configuration

| Component           | XIAO RA4M1 Pin |
|---------------------|----------------|
| Solenoid Valve      | D2             |
| Liquid Level Sensor | A0             |

## How It Works

1. The system continuously reads the analog value from the liquid level sensor.
2. The value is converted using a scaling factor.
3. If the measured level rises above the `VENT_THRESHOLD`, the solenoid valve opens to vent air.
4. Once the level falls below the `VENT_RESET_LEVEL`, the solenoid closes.
5. System status and readings are printed to the Serial Monitor every second.

## Configuration Parameters

These can be tuned in the sketch for your specific sensor and desired behaviour:

```cpp
const int VENT_PIN = 2;                  // Output pin for solenoid valve
const int LEVEL_SENSOR_PIN = A0;         // Analog input from liquid level sensor
const float VENT_THRESHOLD = 160.0;      // Upper level to trigger venting
const float VENT_RESET_LEVEL = 80.0;     // Lower level to stop venting
const float ADC_TO_LEVEL = 0.24414;      // ADC to level conversion factor
