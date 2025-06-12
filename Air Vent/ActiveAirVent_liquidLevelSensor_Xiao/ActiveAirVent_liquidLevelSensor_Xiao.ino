// === Pin Definitions ===
const int flowSensorPin = A1;  // Analog pin connected to liquid flow or pressure sensor
const int mosfetPin = D5;      // Digital pin connected to MOSFET gate for solenoid control

// === Thresholds ===
const int flowThreshold = 300; // Trigger solenoid ON when flow reading > 300

// === Control State ===
bool solenoidOn = false;

void setup() {
  Serial.begin(9600);
  pinMode(mosfetPin, OUTPUT);
  digitalWrite(mosfetPin, LOW); // Ensure solenoid is off at start

  Serial.println("Liquid Level Sensor Solenoid Controller Ready");
}

void loop() {
  int flowReading = analogRead(flowSensorPin);

  Serial.print("Flow Level Reading: ");
  Serial.println(flowReading);

  // === Solenoid Control ===
  if (!solenoidOn && flowReading > flowThreshold) {
    digitalWrite(mosfetPin, HIGH); // Turn solenoid ON
    solenoidOn = true;
    Serial.println("Solenoid ON");
  }
  else if (solenoidOn && flowReading <= flowThreshold) {
    digitalWrite(mosfetPin, LOW);  // Turn solenoid OFF
    solenoidOn = false;
    Serial.println("Solenoid OFF");
  }

  delay(100); // Stability delay
}
