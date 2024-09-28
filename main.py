from machine import Pin, time_pulse_us
import utime
import math

# Define pins
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

refresh_speed=0.03 # Refresh speed in sec

speed_of_sound=29.1

# Function to measure distance in cm
def measure_distance():
    # Send a 10us pulse to trigger
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()
    
    # Measure the duration of the echo pulse
    duration = time_pulse_us(echo, 2*refresh_speed)
    if duration<0:
        print('Timed out!')
        return None
    
    # Calculate distance in cm
    distance = (duration / 2) / speed_of_sound # us * cm/us = cm
    return distance

# Main loop
window_size = 500 # Number of samples to average over in order to find the parameters of the distribution
list = [] # List to store the samples of the distribution

caught=False # If an abnormally was detected
while True:
    #utime.sleep(2*refresh_speed)
    distance = measure_distance() # Measure distance
    if not distance: # Check if distance was valid
        continue

    if len(list) > window_size:
        # Steady state is reached, main detection logic here
        # Let's assume that the distance values are gaussian distributed
        mean = sum(list)/len(list)
        squared_data = [(x-mean)**2 for x in list]
        var = sum(squared_data)/len(squared_data)
        standard_div = math.sqrt(var)

        mean_diff = abs(distance-mean)
        rel_threshold = (1.5/100) * mean # Also use a relative threshold to the mean, this avoids being to sensitive
        threshold = max(5*standard_div, rel_threshold)
        if mean_diff > threshold:
            # Detection of abnormaly
            if not caught:
                # First detection of abnormaly
                print(f'Caught! Difference from mean: {mean_diff} cm | threshold: {threshold} cm | mean: {mean} | standard_div: {standard_div}')
                caught=True
            continue # Continue with next measurement, do not add the 'abnomaly' to the statistics
        
        # No abnormaly, now we can safely pop the element, otherwise we would need it in the next iteration
        list.pop(0)
        caught=False
        print(f'Distance: {distance} cm | difference from mean: {mean_diff} cm | threshold: {threshold} cm | mean: {mean} cm | standard_div: {standard_div} cm')
        
    elif len(list) == window_size:
        # Next cycle will be steady state
        print("Training done!")
    else:
        # Add sample to the list
        print(f"Training {len(list)}/{window_size}")
    list.append(distance)

    
