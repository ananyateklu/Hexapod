import Adafruit_PCA9685
import time
import json

# Initialization for first PCA board
pwm1 = Adafruit_PCA9685.PCA9685(address=0x40)
pwm1.set_pwm_freq(60)  # Set frequency to 60hz

# Initialization for second PCA board
pwm2 = Adafruit_PCA9685.PCA9685(address=0x41)
pwm2.set_pwm_freq(60)  # Set frequency to 60hz

# Dictionary to store calibration angles
calibration_data = {
    "PCA_0x40": {},
    "PCA_0x41": {}
}

def set_servo_angle(pwm, channel, angle):
    """ Convert desired angle to PWM pulse and set it for a specific channel """
    pulse = int(angle / 180.0 * 500 + 150)  # Convert angle to pulse
    pwm.set_pwm(channel, 0, pulse)

def calibrate_servo(pwm, board_address, channel):
    """ Ask user for desired angle and set servo to that angle """
    while True:
        angle = float(input(f"Enter angle for servo {channel} on board {board_address} (0 to 180): "))
        set_servo_angle(pwm, channel, angle)
        
        check = input("Are you satisfied with the position? (yes/no): ").strip().lower()
        if check == 'yes':
            # Save the angle to the dictionary
            calibration_data[board_address][channel] = angle
            break

def save_calibration_data(filename="calibration_data.json"):
    """ Save the calibration angles to a file """
    with open(filename, "w") as f:
        json.dump(calibration_data, f)

def move_leg(pwm, channel_base, lift_angle, forward_angle, sideways_angle):
    """ Move a single leg """
    set_servo_angle(pwm, channel_base, lift_angle)  # lift servo
    set_servo_angle(pwm, channel_base + 1, forward_angle)  # forward-backward servo
    set_servo_angle(pwm, channel_base + 2, sideways_angle)  # sideways servo

def walk_cycle():
    # Initial positions, adapt these as needed
    lift_up = 30
    lift_down = 0
    move_forward = 30
    move_backward = -30

    # Step 1: Lift Set 1
    move_leg(pwm1, 0, lift_up, move_backward, 0)  # Front-left leg
    move_leg(pwm1, 3, lift_up, move_backward, 0)  # Mid-right leg
    move_leg(pwm2, 0, lift_up, move_backward, 0)  # Back-left leg
    time.sleep(0.5)

    # Step 2: Move Set 1 forward
    # ... (set forward positions)
    move_leg(pwm1, 0, lift_up, move_forward, 0)  
    move_leg(pwm1, 3, lift_up, move_forward, 0)  
    move_leg(pwm2, 0, lift_up, move_forward, 0)
    time.sleep(0.5)

    # Step 3: Lower Set 1
    # ... (set lower positions)
    move_leg(pwm1, 0, lift_down, move_forward, 0)  
    move_leg(pwm1, 3, lift_down, move_forward, 0)  
    move_leg(pwm2, 0, lift_down, move_forward, 0)
    time.sleep(0.5)

    # TODO Steps 4, 5, and 6 would follow a similar pattern for Set 2

# Test the walking cycle
walk_cycle()

# Main calibration routine for first PCA board
print("Starting calibration for the first PCA board...")
for channel in range(9):  # Calibrate servos 0 to 8
    calibrate_servo(pwm1, "PCA_0x40", channel)

# Main calibration routine for second PCA board
print("Starting calibration for the second PCA board...")
for channel in range(9):  # Calibrate servos 0 to 8
    calibrate_servo(pwm2, "PCA_0x41", channel)

print("Calibration complete!")

# Save the calibration data
save_calibration_data()
