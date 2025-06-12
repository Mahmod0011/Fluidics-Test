const int forcePin = A0;      // Force sensor connected to A0
const int buttonPin = 2;      // Button to initiate calibration

int rawValue = 0;
int zeroCal = 0;
int maxCal = 1023;

bool calibrationDone = false;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP); // Button connected to GND
  Serial.println("Force Sensor Calibration Tool");
  Serial.println("Press and release the button to calibrate...");
}

void loop() {
  // Check for calibration button press
  if (digitalRead(buttonPin) == LOW) {
    calibrateSensor();
  }

  rawValue = analogRead(forcePin);
  
  // Map the raw value to a 0–100% scale using calibration
  int mappedValue = map(constrain(rawValue, zeroCal, maxCal), zeroCal, maxCal, 0, 100);

  Serial.print("Raw: ");
  Serial.print(rawValue);
  Serial.print(" | Calibrated: ");
  Serial.print(mappedValue);
  Serial.println(" %");

  delay(200);
}

void calibrateSensor() {
  Serial.println("\nCalibration started...");

  // Get baseline value
  Serial.println("Release all pressure from sensor. Hold still...");
  delay(2000);
  zeroCal = analogRead(forcePin);
  Serial.print("Zero calibration: ");
  Serial.println(zeroCal);

  // Get max pressure value
  Serial.println("Now press hard on the sensor...");
  delay(3000);
  maxCal = analogRead(forcePin);
  Serial.print("Max calibration: ");
  Serial.println(maxCal);

  // Ensure values are reasonable
  if (maxCal <= zeroCal) {
    maxCal = zeroCal + 10;
    Serial.println("Warning: max too close to zero, adjusted automatically.");
  }

  calibrationDone = true;
  Serial.println("Calibration complete.\n");
}
