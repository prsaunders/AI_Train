from IOPi import IOPi
import RPi.GPIO as GPIO
gpio_ver = GPIO.VERSION
import threading
from time import sleep
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
#from adafruit_servokit import ContinuousServo
#kitc = ContinuousServo
from adafruit_servokit import PCA9685
#import signal
import buttonshim

# Train Detector settings
TrnDet = IOPi(0x20)
TrnDet.set_bus_direction(0xFFFF)
TrnDet.set_port_pullups(0, 0xFF)
TrnDet.set_port_pullups(1, 0xFF)

# Train Signal Settings
TrnSig = IOPi(0x21)
TrnSig.set_bus_direction(0X0)
green = 2
red = 1

# Switch Settings
SW_Min = 1322
SW_MinDeg = 58
SW_Max = 1556
SW_MaxDeg = 100
SW_Main = 0
SW_TurnOut = 1

# Boom (Barrier) Settings
BM_Min = 1162
BM_Min_Deg = 30
BM_Max = 1711
BM_Max_Deg = 128
BM_Up = 0
BM_Down = 1

# Train Layout Data
SwitchCT = 8        # Channels 1 to 12  (12 max)
BoomCT   = 1        # Channels 13 to 16 (4 max)
TrainDET = 6        # Detectors 1 to 16 (16 max)
TrainSIG = 7        # Signals 1 to 8    (8 max) More reqires another IO_Pi Bd + Plus Interface Bd

@buttonshim.on_release(buttonshim.BUTTON_A)
def button_a(button, pressed):
    global button_flag
    button_flag = 'A'

@buttonshim.on_release(buttonshim.BUTTON_B)
def button_b(button, pressed):
    global button_flag
    button_flag = 'A'

@buttonshim.on_release(buttonshim.BUTTON_C)
def button_c(button, pressed):
    global button_flag
    button_flag = 'C'

@buttonshim.on_release(buttonshim.BUTTON_D)
def button_d(button, pressed):
    global button_flag
    button_flag = 'D'

@buttonshim.on_release(buttonshim.BUTTON_E)
def button_e(button, pressed):
    global button_flag
    button_flag = 'E'

def MainMenu():
    print()
    print()
    print('Available Tests:')
    print('     A: Switch and Boom Tests')
    print('     B: Boom Tests')
    print('     C: Track Lights - Train Detector Tests')
    print('     D: ')
    print('     E: Testing Done')

def Menu_1():
    print("\nPress: A: to set Actuation Range (degrees)")
    print("       E: to finish test")

def Menu_2():
    print("\nPress: A: to move to 0 degrees")
    print("       B: to move to Actuation Max")
    print("       C: to set Min/Max range")
    print("       D: to set Angle")
    print("       E: to finish test")

def Menu_3():
    print("\nPress: A: Toggle Green and Red")
    print("       B: Flash Green and Red")
    print("       C: Train Detector (Grn = Train1 / Red = Train2")
    print("       D: next group")
    print("       E: to finish test")

def SetSW_minmax(sw):
    kit.servo[sw].set_pulse_width_range(SW_Min, SW_Max)

def SetBM_minmax(bm):
    kit.servo[bm].set_pulse_width_range(BM_Min, BM_Max)

def Switch_Control(sw, pos):
    if (pos == SW_Main):                    # main line
        kit.servo[sw].angle = SW_MaxDeg
    else:                                   # turnout
        kit.servo[sw].angle =  SW_MinDeg

def Boom_Control(bm, pos):
    if (pos == BM_Up):
        kit.servo[bm].angle = BM_Max_Deg
    else:
        kit.servo[bm].angle = BM_Min_Deg


# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main():
    global Rotary_counter, LockRotary, button_flag, loop, sMin, sMax

    button_flag = 'null'
    Tst = 0                     # Test number running
    sdir = 1                    # Servo Test Direction
    sMin = 0                    # Servo Minimum Angle
    sMax = 0                    # Servo Maximum Angle

    # setup layout Switches min/max
    for sw in range(SwitchCT):
        kit.servo[sw].set_pulse_width_range(SW_Min, SW_Max)
    
    # setup layout Barriers
    for bm in range(BoomCT):
        kit.servo[bm].set_pulse_width_range(BM_Min, BM_Max)

    MainMenu()
    while True:                                     # start test
        if button_flag == 'A':
            button_flag = 'null'
        elif button_flag == 'B':
            button_flag = 'null'
        elif button_flag == 'C':
            button_flag = 'null'
        elif button_flag == 'D':
            button_flag = 'null'
        elif button_flag == 'E':
            print("DONE")
            return


# start main demo function
main()