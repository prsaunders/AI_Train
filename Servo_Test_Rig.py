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
import signal
import buttonshim

#pca = PCA9685(i2c)
#servo = kit.Servo(0)

TrnDet = IOPi(0x20)
TrnDet.set_bus_direction(0xFFFF)
TrnDet.set_port_pullups(0, 0xFF)
TrnDet.set_port_pullups(1, 0xFF)
#TD = TrnDet.read_port(0) + (TrnDet.read_port(1) * 8)

TrnSig = IOPi(0x21)
TrnSig.set_bus_direction(0X0)
#TrnSig.set_port_pullups(0,0xCF)
#TrnSig.set_port_pullups(1,0xFF)


# GPIO Ports
Enc_A = 17 				# Encoder input A: input GPIO 4
Enc_B = 18		        # Encoder input B: input GPIO 14

Rotary_counter = 0  			# Start counting from 0
Current_A = 1					# Assume that rotary switch is not
Current_B = 1					# moving while we init software

LockRotary = threading.Lock()		# create lock for rotary switch

TstServo = 0                        # Servo under test channel number

loop = 0

#train1 = 0
#train2 = 0

green = 2
red = 1

group = 1

# initialize interrupt handlers
def init():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)					# Use BCM mode
                                            # define the Encoder switch inputs
    GPIO.setup(Enc_A, GPIO.IN)
    GPIO.setup(Enc_B, GPIO.IN)
                                            # setup callback thread for the A and B encoder
                                            # use interrupts for all inputs
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotary_interrupt)  # NO bouncetime
    GPIO.add_event_detect(Enc_B, GPIO.RISING, callback=rotary_interrupt)  # NO bouncetime
    return

# Rotarty encoder interrupt:
# this one is called for both inputs from rotary switch (A and B)
def rotary_interrupt(A_or_B):
    global Rotary_counter, Current_A, Current_B, LockRotary
													# read both of the switches
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)
                                                            # now check if state of A or B has changed
                                                            # if not that means that bouncing caused it
    if Current_A == Switch_A and Current_B == Switch_B:     # Same interrupt as before (Bouncing)?
        return										        # ignore interrupt!

    Current_A = Switch_A								# remember new state
    Current_B = Switch_B								# for next bouncing check


    if (Switch_A and Switch_B):						# Both one active? Yes -> end of sequence
        LockRotary.acquire()                        # get lock
        if A_or_B == Enc_B:                         # Turning direction depends on
            Rotary_counter += 1						# which input gave last interrupt
        else:										# so depending on direction either
            Rotary_counter -= 1						# increase or decrease counter
        LockRotary.release()						# and release lock
    return											# THAT'S IT

@buttonshim.on_release(buttonshim.BUTTON_A)
def button_a(button, pressed):
    global button_flag
    button_flag = 'b1'

@buttonshim.on_release(buttonshim.BUTTON_B)
def button_b(button, pressed):
    global button_flag
    button_flag = 'b2'

@buttonshim.on_release(buttonshim.BUTTON_C)
def button_c(button, pressed):
    global button_flag
    button_flag = 'b3'

@buttonshim.on_release(buttonshim.BUTTON_D)
def button_d(button, pressed):
    global button_flag
    button_flag = 'b4'

@buttonshim.on_release(buttonshim.BUTTON_E)
def button_e(button, pressed):
    global button_flag
    button_flag = 'b5'

# Slew actuation range degrees
def Slew_180_Degrees(sdir, lpct, srate, all=0):
    global button_flag, sMin, sMax, TstServo

    sMin = 180
    sMax = 0
    loop = 0
    while loop < lpct:
        if button_flag == 'b5':
            #button_flag = 'null'
            break
        sMin = 180
        sMax = 0
        loop += 1
        Error = 0
        Err = 0
        lct = 0
        if sdir == 1:
            smin = 0
            smax = kit.servo[TstServo].actuation_range + 1
        else:
            smin = kit.servo[TstServo].actuation_range
            smax = -1
        for di in range(smin, smax, sdir):
            if button_flag == 'b5':
                break
            lct += 1
            kit.servo[TstServo].angle = di
            LockRotary.acquire()                    # get lock for rotary switch
            Encoder = round((Rotary_counter/256)*360,1)	# get counter value in degrees
            LockRotary.release()					# and release lock
            # print('Servo =', di, ', Enc =', Encoder)
            if (Encoder != 0):
                Err += round(((Encoder-di)/Encoder)*100,2)
                Error = round(Err / lct, 2)
                # Error = round(((di - Encoder)/di)*100,2)
            if (all == 1):
                print((di, Encoder, Error))
            if Encoder < sMin:
                sMin = Encoder
            if sMax < Encoder:
                sMax = Encoder
            sleep(srate)
        print('{:4d}' .format(loop) + ':  ' + '{:.2f} {:.2f} {:.2f}' .format(sMin,sMax,Error))
        if button_flag != 'b5':
            if sdir == 1:
                sdir = -1
            else:
                sdir = 1

def MainMenu():
    print()
    print()
    print('Available Tests:')
    print('     A: Servo Range of Motion')
    print('     B: Adjust Servo Range')
    print('     C: Track Lights - Train Detector Tests')
    print('     D: ')
    print('     E: Done')

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

def EncAngErr():
    nenc = round((Rotary_counter/256)*360,1)
    nang = round(kit.servo[TstServo].angle,2)
    if nenc != 0:
        nerr = round(((nenc-nang)/nenc)*100,2)
    else:
        nerr = 0
    print("Enc:", nenc , "Servo:", nang, "Err:", nerr)

# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main():
    global Rotary_counter, LockRotary, button_flag, loop, sMin, sMax

    button_flag = 'null'
    Tst = 0                     # Test number running
    sdir = 1                    # Servo Test Direction
    sMin = 0                    # Servo Minimum Angle
    sMax = 0                    # Servo Maximum Angle

    init()										    # Init interrupts, GPIO, ...

    Encoder = 0
    kit.servo[TstServo].angle = 0
    #kit.continuous_servo[TstServo].throttle
    sleep(1)
    Encoder = 0
    Rotary_counter = 0
    #Range = []
    #Ct = 0

    # set default servo min/max
    kit.servo[TstServo].set_pulse_width_range(700,2300)

    MainMenu()
    while True:                                     # start test
        #Tst = int(input('Enter Test to Run: ' + '\n'))
        #if Tst == 1:
        if button_flag == 'b1':
            button_flag = 'null'
            loop = 0
            print("\nRANGE OF MOTION TEST")
            print("Loop   Min  Max     Error")
            Slew_180_Degrees(1, 100, 0.05)
            if button_flag == 'b5':
                button_flag = 'null'
                print("Range Test Terminated\n")
                Menu_1()
                while button_flag != 'b5':
                    if button_flag == 'b1':
                        button_flag = 'null'
                        actrng = int(input("Enter new Actuation Range (degrees):"))
                        kit.servo[TstServo].actuation_range = actrng
                        MainMenu()
                        sleep(2)
                        break
                    elif button_flag == 'b5':
                        button_flag ='null'
                        MainMenu()
                        sleep(2)    # allow time to release button
                        break
        elif button_flag == 'b2':
            button_flag = 'null'
            loop = 0
            print("\nTEST PWM SETTINGS")
            print("\nDefault settings: 750, 2250")
            print("Range:   ",kit.servo[TstServo].actuation_range)
            print("Fraction:", round(kit.servo[TstServo].fraction, 2))
            print("Angle:   ", round(kit.servo[TstServo].angle))
            Menu_2()
            while button_flag != 'b5':
                if button_flag == 'b1':
                    button_flag = 'null'
                    kit.servo[TstServo].angle = 0
                    sleep(1)
                    EncAngErr()
                    Menu_2()
                elif button_flag == 'b2':
                    button_flag = 'null'
                    kit.servo[TstServo].angle = kit.servo[TstServo].actuation_range
                    sleep(1)
                    EncAngErr()
                    Menu_2()
                elif button_flag == 'b3':
                    button_flag = 'null'
                    minrange = int(input("Enter Minimum Range: "))
                    maxrange = int(input("Enter Maximum Range: "))
                    kit.servo[TstServo].set_pulse_width_range(minrange,maxrange)
                    kit.servo[TstServo].angle = 0
                    sleep(0.5)
                    Encoder = 0
                    Rotary_counter = 0
                    Slew_180_Degrees(1, 2, 0.005)
                elif button_flag == 'b4':
                    newangle = int(input("Enter Angle (0 to 180; -1 to stop): "))
                    if newangle >= 0:
                        kit.servo[TstServo].angle = newangle
                        sleep(0.5)
                        if newangle == 0:
                            Encoder = 0
                            Rotary_counter = 0
                        EncAngErr()
                    else:
                        button_flag = 'null'
                        Menu_2()
                elif button_flag == 'b5':
                    button_flag = 'null'
                    print('\n')
                    MainMenu()
                    sleep(2)
                    break
#            MainMenu()
#            sleep(2)
            button_flag = 'null'
        elif button_flag == 'b3':
            train1 = 0
            train2 = 0
            group = 0
            grp = 0

            button_flag = 'null'
            kit.continuous_servo[8].throttle = 0.0
            kit.continuous_servo[9].throttle = 0.0
            print('\n\nTrack Lights and Train Detector Tests')
            Menu_3()
            while button_flag != 'b5':
                if button_flag == 'b1':
                    if train1 == 0:
                        train1 = 1
                    else:
                        train1 = 0
                    TrnSig.write_pin(group + green, train1)
                    TrnSig.write_pin(group + red, train1)
                    button_flag = 'null'
                elif button_flag == 'b2':
                    if train2 == 0:
                        train2 = 1
                        TrnSig.write_pin(group + red, 0)
                        TrnSig.write_pin(group + green, 1)
                    else:
                        train2 = 0
                        TrnSig.write_pin(group + green, 0)
                        TrnSig.write_pin(group + red, 1)
                    sleep(0.25)
                    #button_flag = 'null'
                elif button_flag == 'b3':
                    #button_flag = 'null'
                    grp = (group * 2)
                    train1 = TrnDet.read_pin(grp + 1)
                    train2 = TrnDet.read_pin(grp + 2)
                    TrnSig.write_pin(grp + green, train1)
                    TrnSig.write_pin(grp + red, train2)
                    #sleep(0.25)
                elif button_flag == 'b4':
                    if group < 7:
                        group += 1
                    else:
                        group = 0
                    print("Move connectors to next group; then press C")
#                    while button_flag != 'b4':
#                        sleep(0.1)
                    button_flag = 'null'
                elif button_flag == 'b5':
                    button_flag = 'null'
                    print('\n')
                    MainMenu()
                    sleep(2)
                    break


        elif button_flag == 'b4':
            button_flag = 'null'
            print('\n\nRunning Test 4')
        elif button_flag == 'b5':
            print("DONE")
            return


# start main demo function
main()