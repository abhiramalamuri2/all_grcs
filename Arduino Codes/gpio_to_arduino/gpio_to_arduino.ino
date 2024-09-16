// Define the GPIO pin on the Arduino that connects to the USRP GPIO output
const int gpioInputPin = 2;  // You can change this to the appropriate pin

void setup() {
  // Initialize the serial communication for output
  Serial.begin(9600);

  // Set the GPIO pin as an input
  pinMode(gpioInputPin, INPUT);
}

void loop() {
  // Read the state of the GPIO pin
  int gpioState = digitalRead(gpioInputPin);

  // Check if the pin is HIGH or LOW and print the result
  if (gpioState == HIGH) {
    Serial.println("HIGH");
  } else {
    Serial.println("LOW");
  }

  // Small delay to prevent spamming the serial monitor
  delay(500);  // Adjust delay if needed
}
