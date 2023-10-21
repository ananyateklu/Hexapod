import Adafruit_PCA9685
import time
import json

# Initialization for first PCA board
pwm1 = Adafruit_PCA9685.PCA9685(address=0x40)
pwm1.set_pwm_freq(60)  # Set frequency to 60hz

# Initialization for second PCA board
pwm2 = Adafruit_PCA9685.PCA9685(address=0x41)
pwm2.set_pwm_freq(60)  # Set frequency to 60hz

# Import your calibration data
calibration_data = {
    "PCA_0x40": {"0": 25.0, "1": 0.0, "2": 0.0, "3": 50.0, "4": 40.0, "5": 50.0, "6": 90.0, "7": 80.0, "8": 50.0},
    "PCA_0x41": {"0": 0.0, "1": 0.0, "2": 0.0, "3": 70.0, "4": 70.0, "5": 40.0, "6": 80.0, "7": 90.0, "8": 90.0}
}

def set_servo_angle(pwm, channel, angle):
    """ Convert desired angle to PWM pulse and set it for a specific channel """
    pulse = int(angle / 180.0 * 500 + 150)  # Convert angle to pulse
    pwm.set_pwm(channel, 0, pulse)

def move_leg(pwm, channel_base, lift_angle_offset, forward_angle_offset, sideways_angle_offset):
    """ Move a single leg using offsets """
    lift_angle = calibration_data["PCA_0x40" if pwm == pwm1 else "PCA_0x41"][str(channel_base)] + lift_angle_offset
    forward_angle = calibration_data["PCA_0x40" if pwm == pwm1 else "PCA_0x41"][str(channel_base + 1)] + forward_angle_offset
    sideways_angle = calibration_data["PCA_0x40" if pwm == pwm1 else "PCA_0x41"][str(channel_base + 2)] + sideways_angle_offset
    set_servo_angle(pwm, channel_base, lift_angle)  # lift servo
    set_servo_angle(pwm, channel_base + 1, forward_angle)  # forward-backward servo
    set_servo_angle(pwm, channel_base + 2, sideways_angle)  # sideways servo

def walk_cycle():
    # Offsets for movements, adapt these as needed
    lift_up_offset = 30
    lift_down_offset = -30
    move_forward_offset = 20
    move_backward_offset = -20

    # Step 1: Lift Set 1 (Front-left, Mid-right, Back-left)
    move_leg(pwm1, 0, lift_up_offset, 0, 0)  
    move_leg(pwm1, 3, lift_up_offset, 0, 0)  
    move_leg(pwm2, 0, lift_up_offset, 0, 0)
    time.sleep(0.25)  # Wait for 250 milliseconds

    # Step 2: Move Set 1 forward
    move_leg(pwm1, 0, 0, move_forward_offset, 0)  
    move_leg(pwm1, 3, 0, move_forward_offset, 0)  
    move_leg(pwm2, 0, 0, move_forward_offset, 0)
    time.sleep(0.25)

    # Step 3: Lower Set 1
    move_leg(pwm1, 0, lift_down_offset, 0, 0)  
    move_leg(pwm1, 3, lift_down_offset, 0, 0)  
    move_leg(pwm2, 0, lift_down_offset, 0, 0)
    time.sleep(0.25)

    # Step 4: Lift Set 2 (Front-right, Mid-left, Back-right)
    move_leg(pwm1, 1, lift_up_offset, 0, 0)  
    move_leg(pwm1, 4, lift_up_offset, 0, 0)  
    move_leg(pwm2, 1, lift_up_offset, 0, 0)
    time.sleep(0.25)

    # Step 5: Move Set 2 forward
    move_leg(pwm1, 1, 0, move_forward_offset, 0)  
    move_leg(pwm1, 4, 0, move_forward_offset, 0)  
    move_leg(pwm2, 1, 0, move_forward_offset, 0)
    time.sleep(0.25)

    # Step 6: Lower Set 2
    move_leg(pwm1, 1, lift_down_offset, 0, 0)  
    move_leg(pwm1, 4, lift_down_offset, 0, 0)  
    move_leg(pwm2, 1, lift_down_offset, 0, 0)
    time.sleep(0.25)

def walk_cycle():
    # Offsets for movements, adapt these as needed
    lift_up_offset = 30
    lift_down_offset = -30
    move_forward_offset = 20
    move_backward_offset = -20

    # Step 1: Lift Set 1 (Front-left, Mid-right, Back-left)
    move_leg(pwm1, 0, lift_up_offset, 0, 0)  
    move_leg(pwm1, 3, lift_up_offset, 0, 0)  
    move_leg(pwm2, 0, lift_up_offset, 0, 0)
    time.sleep(0.25)  # Wait for 250 milliseconds

    # Step 2: Move Set 1 forward
    move_leg(pwm1, 0, 0, move_forward_offset, 0)  
    move_leg(pwm1, 3, 0, move_forward_offset, 0)  
    move_leg(pwm2, 0, 0, move_forward_offset, 0)
    time.sleep(0.25)

    # Step 3: Lower Set 1
    move_leg(pwm1, 0, lift_down_offset, 0, 0)  
    move_leg(pwm1, 3, lift_down_offset, 0, 0)  
    move_leg(pwm2, 0, lift_down_offset, 0, 0)
    time.sleep(0.25)

    # Step 4: Lift Set 2 (Front-right, Mid-left, Back-right)
    move_leg(pwm1, 1, lift_up_offset, 0, 0)  
    move_leg(pwm1, 4, lift_up_offset, 0, 0)  
    move_leg(pwm2, 1, lift_up_offset, 0, 0)
    time.sleep(0.25)

    # Step 5: Move Set 2 forward
    move_leg(pwm1, 1, 0, move_forward_offset, 0)  
    move_leg(pwm1, 4, 0, move_forward_offset, 0)  
    move_leg(pwm2, 1, 0, move_forward_offset, 0)
    time.sleep(0.25)

    # Step 6: Lower Set 2
    move_leg(pwm1, 1, lift_down_offset, 0, 0)  
    move_leg(pwm1, 4, lift_down_offset, 0, 0)  
    move_leg(pwm2, 1, lift_down_offset, 0, 0)
    time.sleep(0.25)

# Test the walking cycle
walk_cycle()

