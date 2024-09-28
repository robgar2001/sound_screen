# Sound Screen
### Detection of a person using HC-SR04 and Raspberry Pi Pico
It is a simple MicroPython script to detect humans passing in front of the HC-SR04 connected sensor. The principle is based on detecting the anomaly as a deviation from the expected statistical distribution: a gaussian distribution.

* main.py: The MicroPython logic.

* feedback.py: Can be used to play a beeping tone on an computer when passing in front of the sensor.

### Hardware

* Raspberry Pi Pico

* HC-SR04

* Breadboard

Connect Vcc and GND to the HC-SR04 sensor. The trigger pin can be connected directly to GPIO pin 3. Carefull, the echo pin should be connected via a voltage divider to GPIO pin 3. This since the pico utilizes 3V3 logic instead of the 5V from the sensor. I used 3.3K and 5.8K for the voltage divider.

### Results
During testing, I managed to get accurate detection up to 370 cm. Further than 370 cm wasn't tested.
