
import Adafruit_PCA9685
import time

# Initialization for PCA board
pwm = Adafruit_PCA9685.PCA9685(address=0x40)
pwm.set_pwm_freq(60)  # Set frequency to 60hz

def set_servo_angle(pwm, pin, angle, calibration_offset=0.0):
    servo_min = 150
    servo_max = 600
    angle = max(min(angle, 180), 0)
    angle += calibration_offset
    pulse_length = int(((servo_max - servo_min) / 180.0) * angle + servo_min)
    pwm.set_pwm(pin, 0, pulse_length)

def lift_legs(pwm, side, lift_angle=30):
    left_leg_pins = [0, 3, 6]
    right_leg_pins = [1, 4, 7]
    pins_to_lift = left_leg_pins if side == 'left' else right_leg_pins if side == 'right' else []
    for pin in pins_to_lift:
        set_servo_angle(pwm, pin, lift_angle)

def move_legs(pwm, side, move_angle=30):
    left_mid_pins = [3, 4, 5]
    right_mid_pins = [9, 10, 11]
    pins_to_move = left_mid_pins if side == 'left' else right_mid_pins if side == 'right' else []
    for pin in pins_to_move:
        set_servo_angle(pwm, pin, move_angle)

def drop_legs(pwm, side, drop_angle=0):
    left_leg_pins = [0, 3, 6]
    right_leg_pins = [1, 4, 7]
    pins_to_drop = left_leg_pins if side == 'left' else right_leg_pins if side == 'right' else []
    for pin in pins_to_drop:
        set_servo_angle(pwm, pin, drop_angle)

def shift_weight(pwm, side, shift_angle=15):
    body_pins = [6, 7, 8]
    shift_direction = 1 if side == 'left' else -1 if side == 'right' else 0
    for pin in body_pins:
        current_angle = 90
        new_angle = current_angle + (shift_direction * shift_angle)
        set_servo_angle(pwm, pin, new_angle)

def walk_cycle(pwm, steps=1, delay=0.5):
    for _ in range(steps):
        lift_legs(pwm, 'right')
        time.sleep(delay)
        move_legs(pwm, 'right')
        time.sleep(delay)
        drop_legs(pwm, 'right')
        time.sleep(delay)
        shift_weight(pwm, 'right')
        time.sleep(delay)
        lift_legs(pwm, 'left')
        time.sleep(delay)
        move_legs(pwm, 'left')
        time.sleep(delay)
        drop_legs(pwm, 'left')
        time.sleep(delay)
        shift_weight(pwm, 'left')
        time.sleep(delay)

# Execute the walk_cycle function to make the hexapod walk
walk_cycle(pwm, steps=3, delay=0.5)
