#include "sensirion-lf.h"

#define SOLENOID_PIN 5
#define MEASURE_DELAY 100  // ms

// Detection threshold (adjust based on your real-world flow baseline)
#define FLOW_MIN_THRESHOLD 1.0   // ml/min
#define BUBBLE_DETECTION_DURATION 200  // ms window to confirm bubble

bool solenoidState = false;
unsigned long bubbleStartTime = 0;
bool bubbleDetected = false;

void setup() {
  Serial.begin(115200);
  pinMode(SOLENOID_PIN, OUTPUT);
  digitalWrite(SOLENOID_PIN, LOW);

  if (SLF3X.init() != 0) {
    Serial.println("❌ Error initializing SLF3X sensor.");
    while (1) delay(1000);
  }

  Serial.println("💡 Send '1' to turn valve ON, '0' to turn it OFF.");
}

void loop() {
  // === Serial command for solenoid ===
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == '1') {
      digitalWrite(SOLENOID_PIN, HIGH);
      solenoidState = true;
      Serial.println("🔧 Valve ON");
    } else if (cmd == '0') {
      digitalWrite(SOLENOID_PIN, LOW);
      solenoidState = false;
      Serial.println("🔧 Valve OFF");
    }
  }

  // === Read flow sensor ===
  if (SLF3X.readSample() == 0) {
    float flow = SLF3X.getFlow() * 19.0;  // to ml/min
    float temp = SLF3X.getTemp();

    // Air bubble detection logic
    if (flow < FLOW_MIN_THRESHOLD) {
      if (!bubbleDetected) {
        if (bubbleStartTime == 0) {
          bubbleStartTime = millis();
        } else if (millis() - bubbleStartTime > BUBBLE_DETECTION_DURATION) {
          bubbleDetected = true;
          Serial.println("🫧 Air bubble detected!");
        }
      }
    } else {
      bubbleStartTime = 0;
      bubbleDetected = false;
    }

    // === Output ===
    Serial.print("Flow: ");
    Serial.print(flow, 2);
    Serial.print(" ml/min | Temp: ");
    Serial.print(temp, 1);
    Serial.print(" °C | Valve: ");
    Serial.print(solenoidState ? "ON" : "OFF");
    Serial.print(" | AirBubble: ");
    Serial.println(bubbleDetected ? "YES" : "NO");
  } else {
    Serial.println("⚠️ Sensor read error");
  }

  delay(MEASURE_DELAY);
}
