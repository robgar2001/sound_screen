# Make a beeping sound when the intruder is detected!
import serial
from playsound import playsound

# Open the serial port
ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
    # Read a line from the serial port
    line = ser.readline().decode('utf-8').strip()
    print(line)

    # Check if the line contains "Caught!"
    if "Caught!" in line:
        # Play a sound
        playsound('beep.mp3')

