IOPI_Full = True

import os
import sys

from PyQt5 import QtWidgets, QtCore, QtGui, uic
# # from PyQt5 import qtbluetooth as QtBt
from PyQt5.QtGui import QPalette, QColor    #, QTextBlock
from PyQt5.QtWidgets import QApplication, QMainWindow   #, QLabel, QGridLayout, QFormLayout, QTableWidgetItem
# rom PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QDialog # , QTextEdit, QListView, QListWidget
# from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt # , QEvent, QFileSelector, QTimerEvent

from IOPi import IOPi
import RPi.GPIO as GPIO

import threading

from time import sleep, time, ctime

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
from adafruit_servokit import PCA9685

from datetime import datetime

from Configurator import Ui_mwTester
from FileOpen import Ui_dlgFileOpen
from FileSave import Ui_dlgFileSave

from FileOpen import Ui_dlgFileOpen
from FileSave import Ui_dlgFileSave

TrackInventoryVer = 0.0
TrackStateVer = 0.0
# CurSessionName = "CurSession"

# Train Detector settings
TrnDet = IOPi(0x20)
TrnDet.set_bus_direction(0xFFFF)
TrnDet.set_port_pullups(0, 0xFF)
TrnDet.set_port_pullups(1, 0xFF)
TrnDet.invert_bus(0xFFFF)

# Train Signal Settings
TrnSigM = IOPi(0x21)
TrnSigM.set_bus_direction(0X0)
TrnSigM.invert_bus(0xFFFF)
# Second Card
TrnSigL = IOPi(0x22)
TrnSigL.set_bus_direction(0X0)
TrnSigL.invert_bus(0xFFFF)
TrnSigW = IOPi(0x23)
TrnSigW.set_bus_direction(0X0)
TrnSigW.invert_bus(0xFFFF)

# Switch Settings
SW_Min = 1322
SW_MinDeg = 58
SW_Max = 1556
SW_MaxDeg = 100
SW_Main = "M"
SW_Spur = "S"
TO_Left = "L"
TO_Right = "R"
TO_Wye = "W"
SW_Chan = 0
# Boom (Barrier) Settings
Boom = "B"
BM_Min = 1162
BM_Min_Deg = 0  #30
BM_Max = 1711
BM_Max_Deg = 90 #128
BM_Up = "U"
BM_Down = "D"
BM_Chan = 0
#global SV_Type
SV_Type = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
#global SV_State
SV_State = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]

# Train Detector Settings
#global TD_Type
TD_Type = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
#global TD_State
TD_State = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
TD_Chan = 0

# Train SIgnal Settings
TS_Green = "G"
TS_Yellow = "Y"     # toggles Green/Red
TS_Red = "R"
TS_Off = "O"        # off
TS_On = "3"         # 3 = string 1 & string 2
TS_O1 = "1"         # 1 = string 1
TS_O2 = "2"         # 2 = string 2
TS_FlashR = "F"     # causes flashing reds Boom Lights    

#           0                                       1                                       2
#           1    2    3    4    5    6    7    8    1    2    3    4    5    6    7    8    1    2    3    4    5    6    7    8
#global TS_Type:    "S" == Signal, "B" == Boom Signal, "F" == Facility (general lighting), " " == Not Defined
TS_Type = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
#global TS_State:   (see above) 
TS_State = ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]
TS_Ind = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#global TS_Time
TS_Time = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

TS_Chan = 0

# Train Layout Data Max values
ServoCT = 16        # Channels 1 to 16  (16 max)
TrainDET = 16       # Detectors 1 to 16 (16 max)
TrainSIG = 8        # Signals 1 to 8    (8 max) More reqires another IO_Pi Bd + Plus Interface Bd CHG
SigState = ""

# train MACs
greentrain = '90:84:2B:BE:F5:DD'
yellowtrain = '90:84:28:22:FC:3F'
loneranger = '90:84:2B:0C:22:02'
x = 0

# def Connect_To_Train(TMac):
#     # conn = get_connection_auto()
#     # try:
#     #     h = Hub(conn)
#     #     return(h)
#     # finally:
#     #     conn.disconnect()

#     #conn = get_connection_bluepy(hub_mac=TMac)
#     h = SmartHub()
#     return(h)

def TS_Blinker():
    global TS_Type, TS_State, TS_Time, TS_Ind
    
    rng = 23
    for i in range(rng):
        if TS_State[i] == TS_Yellow or TS_State[i] == TS_FlashR:
            t = int(TS_Time[i])
            if t == 0:
                if TS_Ind[i] == 0:
                    TS_Ind[i] = 1
                else:
                    TS_Ind[i] = 0
                TS_Time[i] = 10
            else:
                t -= 1
                TS_Time[i] = t
        state = TS_Ind[i]
        pin = ((i*2)+1)
        if i < 8:
            TS = TrnSigM
        elif i < 16:
            pin = (((i-8)*2)+1)
            TS = TrnSigL
        else:
            pin = (((i-16)*2)+1)
            TS = TrnSigW

        if i == w.ui.sbSL_Chan.value()-1:
            if TS_State[i] == TS_Green:
                TS.write_pin(pin, 0)    # green on
                w.ui.rbSL_Top.setPalette(palGreen)
                TS.write_pin(pin+1,1)   # red off
                w.ui.rbSL_Bottom.setPalette(palBlk)
            elif TS_State[i] == TS_Red:
                TS.write_pin(pin+1, 0)  # red on
                w.ui.rbSL_Bottom.setPalette(palRed)
                TS.write_pin(pin, 1)    # green off
                w.ui.rbSL_Top.setPalette(palBlk)
            elif TS_State[i] == TS_FlashR:
                TS.write_pin(pin, 1)        # green off
                w.ui.rbSB_Left.setPalette(palBlk)
                TS.write_pin(pin+1,state)   # flashing red
                if state == 0:
                    w.ui.rbSB_Right.setPalette(palRed)
                else:
                    w.ui.rbSB_Right.setPalette(palBlk)
            elif TS_State[i] == TS_Yellow:
                if state==1:
                    # green on
                    TS.write_pin(pin, 1)
                    TS.write_pin((pin+1), 0)
                    if w.ui.cbTS_Type.currentText()[0] == "S":
                        w.ui.rbSL_Bottom.setPalette(palBlk)
                        w.ui.rbSL_Top.setPalette(palGreen)
                    else:
                        w.ui.rbSB_Left.setPalette(palBlk)
                        w.ui.rbSB_Right.setPalette(palRed)
                else:
                    TS.write_pin(pin, 0)
                    TS.write_pin((pin+1), 1)
                    if w.ui.cbTS_Type.currentText()[0] == "S":
                        w.ui.rbSL_Bottom.setPalette(palRed)
                        w.ui.rbSL_Top.setPalette(palBlk)
                    else:
                        w.ui.rbSB_Left.setPalette(palRed)
                        w.ui.rbSB_Right.setPalette(palBlk)
            elif TS_State[i] == TS_Off:
                TS.write_pin(pin, 1)
                w.ui.rbSF_Left .setPalette(palBlk)
                w.ui.rbSB_Left .setPalette(palBlk)
                TS.write_pin(pin+1,1)
                w.ui.rbSB_Right.setPalette(palBlk)
                w.ui.rbSF_Right .setPalette(palBlk)
            elif TS_State[i] == TS_On:
                TS.write_pin(pin, 0)
                w.ui.rbSF_Left .setPalette(palYellow)
                TS.write_pin(pin+1,0)
                w.ui.rbSF_Right .setPalette(palYellow)
            elif TS_State[i] == TS_O1:
                TS.write_pin(pin, 0)
                w.ui.rbSF_Left .setPalette(palYellow)
                TS.write_pin(pin+1,1)
                w.ui.rbSF_Right .setPalette(palBlk)
            elif TS_State[i] == TS_O2:
                TS.write_pin(pin, 1)
                w.ui.rbSF_Left .setPalette(palBlk)
                TS.write_pin(pin+1,0)
                w.ui.rbSF_Right .setPalette(palYellow)
        else:
            if TS_State[i] == TS_Green:
                TS.write_pin(pin, 0)    # green on
                TS.write_pin(pin+1,1)   # red off
            elif TS_State[i] == TS_Red:
                TS.write_pin(pin+1, 0)  # red on
                TS.write_pin(pin, 1)    # green off
            elif TS_State[i] == TS_FlashR:
                TS.write_pin(pin, 1)        # green off
                TS.write_pin(pin+1,state)   # flashing red
            elif TS_State[i] == TS_Yellow:
                if state==1:
                    # green on
                    TS.write_pin(pin, 1)
                    TS.write_pin((pin+1), 0)
                else:
                    TS.write_pin(pin, 0)
                    TS.write_pin((pin+1), 1)
            elif TS_State[i] == TS_Off:
                TS.write_pin(pin, 1)
                TS.write_pin(pin+1,1)
            elif TS_State[i] == TS_On:
                TS.write_pin(pin, 0)
                TS.write_pin(pin+1,0)

TS_Timer = threading.Timer(0.250, TS_Blinker)

def Servo_Control(sv, pos, typ):
    if ((typ == TO_Right) or (typ == TO_Wye)):
        if (pos == SW_Main):                    # main line
            kit.servo[sv].angle = SW_MinDeg
        else:                                   # turnout
            kit.servo[sv].angle =  SW_MaxDeg
    elif (typ == TO_Left):
        if (pos == SW_Main):                    # main line
            kit.servo[sv].angle = SW_MaxDeg
        else:                                   # turnout
            kit.servo[sv].angle =  SW_MinDeg
    elif (typ == Boom):
        if (pos == BM_Up):
            kit.servo[sv].angle = BM_Min_Deg
        else:
            kit.servo[sv].angle = BM_Max_Deg
    SV_State[sv] = pos

palGreen = QPalette()
palGreen.setColor(QPalette.Button, Qt.green)
palBlue = QPalette()
palBlue.setColor(QPalette.Button, Qt.blue)
palRed = QPalette()
palRed.setColor(QPalette.Button, Qt.red)
palYellow = QPalette()
palYellow.setColor(QPalette.Button, Qt.yellow)
palBlank = QPalette()
palBlank.setColor(QPalette.Button, QColor(237,237,237))
palBlk = QPalette()
palBlk.setColor(QPalette.Button, QColor(155,173,179))
palBlack = QPalette()
palBlack.setColor(QPalette.WindowText, Qt.black)
palBlnk = QPalette()
palBlnk.setColor(QPalette.WindowText, QColor(237,237,237))

def ReadDetector(chan):
    global  TD_Type, TD_State

    det = TrnDet.read_pin(chan+1)
    TD_State[chan] = det
    w.ui.lblTD_State.setText(str(TD_State).strip("[]"))
    if TD_Type[chan] != " ":
        if TD_State[chan]:
            w.ui.rbTD.setPalette(palBlue)
        else:
            w.ui.rbTD.setPalette(palBlk)

# read and load track inventory file
def Load_Track_Inventory():
    global SV_Type, TS_Type, TD_Type, TrackInventoryVer

    TrackInventoryVer = 0.0
    filename = "Track_Inventory.txt"    
    try:
        f = open(filename)
        lines = f.readlines()
        line = lines[3]
        TrackInventoryVer = float(line.strip("\n"))

        line = lines[8].strip("\n")
        SV_Type = line.split(", ")
        if SV_Type[15] == "":
            SV_Type[15] = " "

        line = lines[11].strip("\n")
        TD_Type = line.split(", ")
        if TD_Type[15] == "":
            TD_Type[15] = " "

        line = lines[14].strip("\n")
        TS_Type = line.split(", ")
        if TS_Type[23] == "":
            TS_Type[23] = " "
        f.close()
        TS_Blinker()
        w.ui.lblTD_Type.setText(str(TD_Type).strip("[]"))
        # if TD_Type[0] == "D":
        #     w.ui.ckbTD_Set.setCheckState(2)
        showTD_Settings()
        w.ui.lblSV_Type.setText(str(SV_Type).strip("[]"))
        showSV_Settings()
        w.ui.lblTS_Type.setText(str(TS_Type).strip("[]"))
        showTS_Settings()
        w.ui.lblTD_State.setText(str(TD_State).strip("[]"))
        w.ui.lblSV_State.setText(str(SV_State).strip("[]"))
        w.ui.lblTS_State.setText(str(TS_State).strip("[]"))
    except:
        filename = ""
        TrackInventoryVer = 0.0

def Save_Train_Inventory():
    global TrackInventoryVer, SV_Type, TS_Type, TD_Type

    # SAVE Train Inventory Data
    # Change name of current invertory file to *.bak
    # try:
    #     f = open("Track_Inventory.bak")
    #     f.close()
    #     os.remove("Track_Inventory.bak")
    #     os.rename("Track_Inventory.txt", "Track_Inventory.bak")
    # except:
    #     #f.close()
    #     print("No Previous Backup File")

    try:
        fBak = "./Track_Inventory.bak"
        fNew = "./Track_Inventory.txt"
        if os.path.exists(fBak):
            os.remove(fBak)
        os.rename(fNew, fBak)
    except:
        #f.close()
        print("No Previous Backup File")
    # Save the results to the inventory file
    # open new file
    f = open("./Track_Inventory.txt", "wt")
    f.write("Track Inventory Data\n\n")

    # Update and write version
    f.write("Version:\n")
    f.write("{:5.3f}".format(TrackInventoryVer + 0.001) + "\n\n")

    # write time stamp
    t = time()
    ct = ctime()
    f.write(ct + "\n\n")

    # Write Inventory Data
    # Save Servo Data
    f.write("Servo Data:\n")
    line = ""
    ct = 0
    ct = len(SV_Type)
    x = 0
    while x < ct:
        line = line + SV_Type[x]
        if x < (ct-1):
            line += ", "
        x += 1
    f.write(line)
    f.write("\n\n")

    # Save Train Detector Data
    line = ""
    ct = len(TD_Type)
    x = 0
    f.write("Train Detector Data:\n")
    while x < ct:
        line = line + TD_Type[x]
        if x < (ct-1):
            line += ", "
        x += 1
    f.write(line) 
    f.write("\n\n")

    # Save Train Signal Data
    line = ""
    ct = len(TS_Type)
    x = 0
    f.write("Train Signal Data:\n")
    while x < ct:
        line = line + TS_Type[x]
        if x < (ct-1):
            line += ", "
        x += 1
    f.write(line) 
    f.write("\n\n")

    f.close()

def Save_Train_State(fN):
    global  TrackStateVer, SV_State, TS_State, TD_Type, \
            SV_Type, TS_Type, TD_Type, TrackInventoryVer

    # Change name of current invertory file to *.bak
    fN = "Track_Inventory"
    try:
        fBak = "./"+fN+".bak"
        fNew = "./"+fN+".ses"
        if os.path.exists(fBak):
            os.remove(fBak)
        os.rename(fNew, fBak)
    except:
        #f.close()
        print("No Previous Backup File")

    # Save the results to the inventory file
    # open new file
    f = open(fN, "wt")
    f.write("Session State\n\n")

    # Update and write version
    f.write("Version:\n")
    f.write("{:5.3f}".format(TrackStateVer + 0.001) + "\n\n")

    # write time stamp
    t = time()
    ct = ctime()
    f.write(ct + "\n\n")

    # Write Inventory State
    # Save Servo State
    f.write("Servo State:\n")
    line = ""
    ct = 0
    ct = len(SV_State)
    x = 0
    while x < ct:
        line = line + SV_State[x]
        if x < (ct-1):
            line += ", "
        x += 1
    f.write(line)
    f.write("\n\n")

    # Save Train Detector State
    line = ""
    ct = len(TD_State)
    x = 0
    f.write("Train Detector State:\n")
    while x < ct:
        line = line + str(TD_State[x])
        if x < (ct-1):
            line += ", "
        x += 1
    f.write(line) 
    f.write("\n\n")

    # Save Train Signal State
    line = ""
    ct = len(TS_State)
    x = 0
    f.write("Train Signal State:\n")
    while x < ct:
        line = line + TS_State[x]
        if x < (ct-1):
            line += ", "
        x += 1
    f.write(line) 
    f.write("\n\n")

    f.close()

def modTD_Settings():
    chan = w.ui.sbTD_Chan.value()-1
    type = w.ui.cbTD_Type.currentText()[0]
    if type != TD_Type[chan]:
        TD_Type[chan] = type

def setTD_Settings():
    chan = w.ui.sbTD_Chan.value()-1
    if w.ui.ckbTD_Set.checkState() == 2:
        TD_Type[chan] = w.ui.cbTD_Type.currentText()[0]
    else:
        TD_Type[chan] = " "
    w.ui.lblTD_Type.setText(str(TD_Type).strip("[]"))
    showTD_Settings()

def showTD_Settings():
    chan = w.ui.sbTD_Chan.value()-1
    type = TD_Type[chan]
    if type != " ":
        if type == "D":
            w.ui.cbTD_Type.setCurrentIndex(0)
        elif type == "S":
            w.ui.cbTD_Type.setCurrentIndex(1)
        ReadDetector(chan)
        if type != w.ui.cbTD_Type.currentText()[0]:
            w.ui.ckbTD_Set.setCheckState(2)
        else:
            w.ui.ckbTD_Set.setCheckState(0)
        w.ui.lblTD_Type.setText(str(TD_Type).strip("[]"))

def setSigType():
    w.ui.gbxSignal.setDisabled(True)
    w.ui.rbSL_Top.setPalette(palBlk)
    w.ui.rbSL_Bottom.setPalette(palBlk)
    w.ui.gbxBoom.setDisabled(True)
    w.ui.rbSB_Left.setPalette(palBlk)
    w.ui.rbSB_Right.setPalette(palBlk)
    w.ui.gbxFacility.setDisabled(True)
    w.ui.rbSF_Left.setPalette(palBlk)
    w.ui.rbSF_Right.setPalette(palBlk)
    type = w.ui.cbTS_Type.currentText()[0]
    chan = w.ui.sbSL_Chan.value()-1
    TS_State[chan] = TS_Off
    TS_Type[chan] = type
    if type == "S":
        w.ui.gbxSignal.setDisabled(False) 
    elif type == "B":
        w.ui.gbxBoom.setDisabled(False)
    elif type == "F":
        w.ui.gbxFacility.setDisabled(False)
    w.ui.lblTS_Type.setText(str(TS_Type).strip("[]"))
    w.ui.lblTS_State.setText(str(TS_State).strip("[]"))
    showTS_Settings()

def setForSignal():
    chan = w.ui.sbSL_Chan.value()-1
    if w.ui.rbSL_Green.isChecked():
        TS_State[chan] = TS_Green
    elif w.ui.rbSL_Red.isChecked():
        TS_State[chan] = TS_Red
    elif w.ui.rbSL_Yellow.isChecked():
        TS_State[chan] = TS_Yellow 
    w.ui.lblTS_State.setText(str(TS_State).strip("[]"))

def setForBoom():
    chan = w.ui.sbSL_Chan.value()-1
    if w.ui.rbSB_On.isChecked():
        TS_State[chan] = TS_Yellow
    elif w.ui.rbSB_Off.isChecked():
        TS_State[chan] = TS_Off
    w.ui.lblTS_State.setText(str(TS_State).strip("[]"))

def setForF1():
    chan = w.ui.sbSL_Chan.value()-1
    TS_State[chan] = TS_O1
    w.ui.lblTS_State.setText(str(TS_State).strip("[]"))

def setForF2():
    chan = w.ui.sbSL_Chan.value()-1
    TS_State[chan] = TS_O2
    w.ui.lblTS_State.setText(str(TS_State).strip("[]"))

def setForBoth():
    chan = w.ui.sbSL_Chan.value()-1
    TS_State[chan] = TS_On
    w.ui.lblTS_State.setText(str(TS_State).strip("[]"))

def setForOff():
    chan = w.ui.sbSL_Chan.value()-1
    TS_State[chan] = TS_Off
    w.ui.lblTS_State.setText(str(TS_State).strip("[]"))

def setTS_Settings():
    chan = w.ui.sbSL_Chan.value()-1
    if w.ui.ckbSL_Set.checkState() == 2:
        TS_Type[chan] = w.ui.cbTS_Type.currentText()[0]
    else:
        TS_Type[chan] = " "
    w.ui.lblTS_Type.setText(str(TS_Type).strip("[]"))
    showTS_Settings()

def showTS_Settings():
    global TS_State, TS_Type

    chan = w.ui.sbSL_Chan.value()-1
    type = TS_Type[chan]        # w.ui.cbTS_Type.currentText()[0]
    if type != " ":
        if type == "S":
            w.ui.cbTS_Type.setCurrentIndex(0) 
        elif type == "B":
            w.ui.cbTS_Type.setCurrentIndex(1)
        elif type == "F":
            w.ui.cbTS_Type.setCurrentIndex(2)
        if type != w.ui.cbTS_Type.currentText()[0]:
            w.ui.ckbSL_Set.setCheckState(2)
        else:
            w.ui.ckbSL_Set.setCheckState(0)

def drawSV(spur, clr):
    pal = QPalette()
    if clr == "B":
        pal = palBlack
    else:
        pal = palBlnk

    if spur == "L":
        w.ui.lL1.setPalette(pal)
        w.ui.lL2.setPalette(pal)
        w.ui.lL3.setPalette(pal)
        w.ui.lL4.setPalette(pal)
    elif spur == "R":
        w.ui.lR1.setPalette(pal)
        w.ui.lR2.setPalette(pal)
        w.ui.lR3.setPalette(pal)
        w.ui.lR4.setPalette(pal)
    elif spur == "M":
        w.ui.lMain.setPalette(pal)
    elif spur == "D":
        w.ui.lBoom.setPalette(pal)

def showSV_Settings():
    chan = w.ui.sbSw_Chan.value()-1
    type = SV_Type[chan]     # w.ui.cbSw_Type.currentText()[0]
    if type != " ":
        if type == "R":
            w.ui.cbSw_Type.setCurrentIndex(0) 
        elif type == "L":
            w.ui.cbSw_Type.setCurrentIndex(1)
        elif type == "W":
            w.ui.cbSw_Type.setCurrentIndex(2)
        elif type == "B":
            w.ui.cbSw_Type.setCurrentIndex(3)
        w.ui.lblSV_Type.setText(str(SV_Type).strip("[]"))

def setSV_Settings():
    chan = w.ui.sbSw_Chan.value()-1
    if w.ui.ckbSW_Set.checkState() == 2:
        SV_Type[chan] = w.ui.cbSw_Type.currentText()[0]
    else:
        SV_Type[chan] = " "
    w.ui.lblSV_Type.setText(str(SV_Type).strip("[]"))
    showSV_Settings()

def SetForMain():
    type =  w.ui.cbSw_Type.currentText()[0]
    if type == "W":
        Servo_Control(w.ui.sbSw_Chan.value()-1,SW_Main,type)
        drawSV("M","b")
        drawSV("L","B")
        drawSV("R","b")
    else:
        if type == "B":
            Servo_Control(w.ui.sbSw_Chan.value()-1,BM_Up,type)
        else:
            Servo_Control(w.ui.sbSw_Chan.value()-1,SW_Main,type)
        drawSV("M","B")
        drawSV("L","b")
        drawSV("R","b")
    drawSV("D","b")
    w.ui.lblSV_State.setText(str(SV_State).strip("[]"))
    showSV_Settings()

def SetForSpur():
    type = w.ui.cbSw_Type.currentText()[0]
    if type != "B":
        Servo_Control(w.ui.sbSw_Chan.value()-1,SW_Spur, type)
        drawSV("M","b")
        drawSV("B","b")
        if type == "L":
            drawSV("L","B")
        elif type == "R":
            drawSV("R","B")
        elif type == "W":
            drawSV("L","b")
            drawSV("R","B")
        w.ui.lblSV_State.setText(str(SV_State).strip("[]"))
        showSV_Settings()

def SetForDown():
    type = w.ui.cbSw_Type.currentText()[0]
    if type == "B":
        Servo_Control(w.ui.sbSw_Chan.value()-1,BM_Down, type)
        drawSV("M","b")
        drawSV("D","B")
        w.ui.lblSV_State.setText(str(SV_State).strip("[]"))
        showSV_Settings()

class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_mwTester()
        self.ui.setupUi(self)

        # Clear rb's
        self.ui.rbSB_Left.setPalette(palBlk)
        self.ui.rbSB_Right.setPalette(palBlk)
        self.ui.rbSF_Left.setPalette(palBlk)
        self.ui.rbSF_Right.setPalette(palBlk)
        self.ui.rbSL_Top.setPalette(palBlk)
        self.ui.rbSL_Bottom.setPalette(palBlk)
        self.ui.rbTD.setPalette(palBlk)
        self.ui.lMain.setPalette(palBlack)
        self.ui.gbxBoom.setDisabled(True)
        self.ui.gbxFacility.setDisabled(True)

        def CloseConfigurator():
            global SessionName
            
#            Save_Train_Inventory()
            self.close()
    
        self.ui.actionOpen_Track_Inventory.triggered.connect(Load_Track_Inventory)
        self.ui.actionSave_Track_Inventory.triggered.connect(Save_Train_Inventory)
        self.ui.actionExit.triggered.connect(CloseConfigurator)

        self.ui.ckbSW_Set.clicked.connect(setSV_Settings)
        self.ui.sbSw_Chan.valueChanged.connect(showSV_Settings)
        self.ui.rbSw_M.clicked.connect(SetForMain)
        self.ui.rbSw_Spur.clicked.connect(SetForSpur)
        self.ui.rbSw_Down.clicked.connect(SetForDown)

        self.ui.ckbTD_Set.clicked.connect(setTD_Settings)
        self.ui.sbTD_Chan.valueChanged.connect(showTD_Settings)
        self.ui.cbTD_Type.currentTextChanged.connect(modTD_Settings)

        self.ui.ckbSL_Set.clicked.connect(setTS_Settings)
        self.ui.sbSL_Chan.valueChanged.connect(showTS_Settings)
        self.ui.cbTS_Type.currentTextChanged.connect(setSigType)
        self.ui.rbSL_Green.clicked.connect(setForSignal)
        self.ui.rbSL_Yellow.clicked.connect(setForSignal)
        self.ui.rbSL_Red.clicked.connect(setForSignal)
        self.ui.rbSB_On.clicked.connect(setForBoom)
        self.ui.rbSB_Off.clicked.connect(setForBoom)
        self.ui.rbSF_1.clicked.connect(setForF1)
        self.ui.rbSF_2.clicked.connect(setForF2)
        self.ui.rbSF_3.clicked.connect(setForBoth)
        self.ui.rbSF_Off.clicked.connect(setForOff)

        self.TTimer = QTimer()
        self.TTimer.timeout.connect(TS_Blinker)
        self.TTimer.start(50)

        # self.DTimer = QTimer()
        # self.DTimer.timeout.connect(ReadDetectors)
        # self.DTimer.start(1000)

app = QApplication(sys.argv)
w = AppWindow()
w.show()
#w.move(1984,0)
sys.exit(app.exec_())
