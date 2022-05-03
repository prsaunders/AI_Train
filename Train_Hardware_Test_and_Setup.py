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

# import RPi.GPIO as GPIO
# import threading
BdsAvailable = ""
from time import sleep, time, ctime

from adafruit_servokit import ServoKit
Servos = True
try:
    kit = ServoKit(channels=16)
    BdsAvailable += "Switches 1-16 :: "
except:
    Servos = False

from adafruit_servokit import PCA9685

from datetime import datetime

from Configurator import Ui_mwTester
from FileOpen import Ui_dlgFileOpen
from FileSave import Ui_dlgFileSave

TrackInventory = "Track_Inventory.txt"
TrackInventoryVer = 0.0
TrackStateVer = 0.0
# CurSessionName = "CurSession"

IOPI_Full = 0
try:
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
    IOPI_Full = 1
    BdsAvailable += "Detectors 1-16 :: Signals 1-8 :: "

    try:
        # Second Card
        TrnSigL = IOPi(0x22)
        TrnSigL.set_bus_direction(0X0)
        TrnSigL.invert_bus(0xFFFF)
        TrnSigW = IOPi(0x23)
        TrnSigW.set_bus_direction(0X0)
        TrnSigW.invert_bus(0xFFFF)

        IOPI_Full = 2
        BdsAvailable += "Signals 9-24"
    except:
        IOPI_Full = IO_PI_Full
except:
    IOPI_Full = 0


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
SV_Type_o = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
#global SV_State
SV_State = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]

# Train Detector Settings
#global TD_Type
TD_Type = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
TD_Type_o = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
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
TS_Type_o = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
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
actv = -1

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

palGreen = QPalette()
palGreen.setColor(QPalette.Button, Qt.green)
palBlue = QPalette()
palBlue.setColor(QPalette.Button, Qt.blue)
palRed = QPalette()
palRed.setColor(QPalette.Button, Qt.red)
palYellow = QPalette()
palYellow.setColor(QPalette.Button, Qt.yellow)
palBlank = QPalette()
palBlank.setColor(QPalette.Button, QColor(155,155,155))
palBlk = QPalette()
palBlk.setColor(QPalette.Button, QColor(155,173,179))
palBlack = QPalette()
palBlack.setColor(QPalette.WindowText, Qt.black)
palRedTxt = QPalette()
palRedTxt.setColor(QPalette.WindowText, Qt.red)
palBlnk = QPalette()                                                                                        
palBlnk.setColor(QPalette.WindowText, QColor(237,237,237))
palGray = QPalette()
palGray.setColor(QPalette.WindowText, QColor(155,155,155))

def TS_Blinker():
    global TS_Type, TS_State, TS_Time, TS_Ind
    
    rng = 24
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
        if IOPI_Full != 0:
            pin = ((i*2)+1)
            if i < 8:
                TS = TrnSigM
            elif i < 16:
                pin = (((i-8)*2)+1)
                TS = TrnSigL
            else:
                pin = (((i-16)*2)+1)
                TS = TrnSigW
        elif IOPI_Full == 2:
            pin = (((i*2)+1)%16)
            TS = TrnSigM
        if i == w.ui.sbSL_Chan.value()-1:
            if TS_State[i] == TS_Green:
                if IOPI_Full >= 1:
                    TS.write_pin(pin, 0)    # green on
                    TS.write_pin(pin+1,1)   # red off
                w.ui.rbSL_Top.setPalette(palGreen)
                w.ui.rbSL_Bottom.setPalette(palBlk)
            elif TS_State[i] == TS_Red:
                if IOPI_Full >= 1:
                    TS.write_pin(pin+1, 0)  # red on
                    TS.write_pin(pin, 1)    # green off
                w.ui.rbSL_Bottom.setPalette(palRed)
                w.ui.rbSL_Top.setPalette(palBlk)
            elif TS_State[i] == TS_FlashR:
                if IOPI_Full >= 1:
                    TS.write_pin(pin, 1)        # green off
                    TS.write_pin(pin+1,state)   # flashing red
                w.ui.rbSB_Left.setPalette(palBlk)
                if state == 0:
                    w.ui.rbSB_Right.setPalette(palRed)
                else:
                    w.ui.rbSB_Right.setPalette(palBlk)
            elif TS_State[i] == TS_Yellow:
                if state==1:
                    # green on
                    if IOPI_Full >= 1:
                        TS.write_pin(pin, 1)
                        TS.write_pin((pin+1), 0)
                    if w.ui.cbTS_Type.currentText()[0] == "S":
                        w.ui.rbSL_Bottom.setPalette(palBlk)
                        w.ui.rbSL_Top.setPalette(palGreen)
                    else:
                        w.ui.rbSB_Left.setPalette(palBlk)
                        w.ui.rbSB_Right.setPalette(palRed)
                else:
                    if IOPI_Full >= 1:
                        TS.write_pin(pin, 0)
                        TS.write_pin((pin+1), 1)
                    if w.ui.cbTS_Type.currentText()[0] == "S":
                        w.ui.rbSL_Bottom.setPalette(palRed)
                        w.ui.rbSL_Top.setPalette(palBlk)
                    else:
                        w.ui.rbSB_Left.setPalette(palRed)
                        w.ui.rbSB_Right.setPalette(palBlk)
            elif TS_State[i] == TS_Off:
                if IOPI_Full >= 1:
                    TS.write_pin(pin, 1)
                    TS.write_pin(pin+1,1)
                w.ui.rbSF_Left .setPalette(palBlk)
                w.ui.rbSB_Left .setPalette(palBlk)
                w.ui.rbSB_Right.setPalette(palBlk)
                w.ui.rbSF_Right .setPalette(palBlk)
            elif TS_State[i] == TS_On:
                if IOPI_Full >= 1:
                    TS.write_pin(pin, 0)
                    TS.write_pin(pin+1,0)
                w.ui.rbSF_Left .setPalette(palYellow)
                w.ui.rbSF_Right .setPalette(palYellow)
            elif TS_State[i] == TS_O1:
                if IOPI_Full >= 1:
                    TS.write_pin(pin, 0)
                    TS.write_pin(pin+1,1)
                w.ui.rbSF_Left .setPalette(palYellow)
                w.ui.rbSF_Right .setPalette(palBlk)
            elif TS_State[i] == TS_O2:
                if IOPI_Full >= 1:
                    TS.write_pin(pin, 1)
                    TS.write_pin(pin+1,0)
                w.ui.rbSF_Left .setPalette(palBlk)
                w.ui.rbSF_Right .setPalette(palYellow)
        else:
            if IOPI_Full >= 1:
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

# TS_Timer = threading.Timer(0.250, TS_Blinker)

def Servo_Control(sv, pos, typ):
    if Servos:
        if ((typ == TO_Right) or (typ == TO_Wye)):
            if (pos == SW_Main):                    # main line
                kit.servo[sv].angle = SW_MinDeg
                sleep(0.2)
                kit.servo[sv].angle = SW_MinDeg + 5
            else:                                   # turnout
                kit.servo[sv].angle = SW_MaxDeg
                sleep(0.2)
                kit.servo[sv].angle = SW_MaxDeg - 5
        elif (typ == TO_Left):
            if (pos == SW_Main):                    # main line
                kit.servo[sv].angle = SW_MaxDeg
                sleep(0.2)
                kit.servo[sv].angle = SW_MaxDeg - 5
            else:                                   # turnout
                kit.servo[sv].angle = SW_MinDeg
                sleep(0.2)
                kit.servo[sv].angle = SW_MinDeg + 5
        elif (typ == Boom):
            if (pos == BM_Up):
                kit.servo[sv].angle = BM_Min_Deg
                sleep(0.2)
                kit.servo[sv].angle = BM_Min_Deg + 5
            else:
                kit.servo[sv].angle = BM_Max_Deg
                sleep(0.2)
                kit.servo[sv].angle = BM_Max_Deg - 5
    SV_State[sv] = pos

def ReadDetectors():
    global TD_Type, TD_State

    for i in range(len(TD_Type)):
        chan = int(i)
        if TD_Type[chan] != " ":
            if IOPI_Full >= 1:
                det = TrnDet.read_pin(chan+1)
            else:
                if TD_State[chan]:
                    det = 0
                else:
                    det = 1
            TD_State[chan] = det
            w.ui.lblTD_State.setText(str(TD_State).strip("[]"))
            if chan == w.ui.sbTD_Chan.value()-1:
                if TD_State[chan]:
                    w.ui.rbTD.setPalette(palYellow)
                else:
                    w.ui.rbTD.setPalette(palBlk)
            # else:
            #     w.ui.rbTD.setPalette(palBlk)

def TestIfModified():
    global TD_Type_o, TD_Type, TS_Type_o, TS_Type, SV_Type_o, SV_Type

    mf = TrackInventory
    if TD_Type_o != TD_Type or TS_Type_o != TS_Type or SV_Type_o != SV_Type:
        mf = mf + " *"
    w.ui.lblFile.setText(mf)

# read and load track inventory file
def Load_Track_Inventory(fname):
    global SV_Type, TS_Type, TD_Type, SV_Type_o, TS_Type_o, TD_Type_o, TrackInventory, TrackInventoryVer

    TrackInventoryVer = 0.0
    if fname != "":
        TrackInventory = fname
    else:
        fname = TrackInventory    
    try:
        f = open(fname)
        lines = f.readlines()
        line = lines[3]
        TrackInventoryVer = float(line.strip("\n"))

        line = lines[8].strip("\n")
        SV_Type = line.split(", ")
        if SV_Type[15] == "":
            SV_Type[15] = " "
        SV_Type_o = line.split(", ")
        if SV_Type_o[15] == "":
            SV_Type_o[15] = " "

        line = lines[11].strip("\n")
        TD_Type = line.split(", ")
        if TD_Type[15] == "":
            TD_Type[15] = " "
        TD_Type_o = line.split(", ")
        if TD_Type_o[15] == "":
            TD_Type_o[15] = " "

        line = lines[14].strip("\n")
        TS_Type = line.split(", ")
        if TS_Type[23] == "":
            TS_Type[23] = " "
        TS_Type_o = line.split(", ")
        if TS_Type_o[23] == "":
            TS_Type_o[23] = " "
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

        # TrackInventory = filename
        w.ui.lblFile.setText(fname)
        TrackInventory = fname
    except:
        filename = ""
        TrackInventoryVer = 0.0

def Save_Track_Inventory(fN):
    global TrackInventoryVer, SV_Type, TS_Type, TD_Type, SV_Type_o, TS_Type_o, TD_Type_o

    # SAVE Train Inventory Data
    # Change name of current invertory file to *.bak
    fNew = ""
    try:
        # get version
        f = open("./"+fN)
        lines = f.readlines()
        line = lines[3]
        TrackStateVer = float(line.strip("\n"))
        
        # back up previous version
        fBak = "./"+fN+".bak"
        fNew = "./"+fN
        if os.path.exists(fBak):
            os.remove(fBak)
        os.rename(fNew, fBak)
    except:
        #f.close()
        fNew = "./"+fN+".txt"
        print("No Previous Backup File")

    # Save the results to the inventory file
    # open new file
    f = open(fNew, "wt")
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

    TrackInventory = fNew
    w.ui.lblFile.setText(fNew)

def modTD_Settings():
    chan = w.ui.sbTD_Chan.value()-1
    dtype = w.ui.cbTD_Type.currentText()[0]
    if dtype != TD_Type[chan]:
        TD_Type[chan] = dtype

def showTD_Settings():
    chan = w.ui.sbTD_Chan.value()-1
    dtype = TD_Type[chan]
    w.ui.rbTD.setPalette(palBlk)
    if dtype != " ":
        if dtype == "D":
            w.ui.cbTD_Type.setCurrentIndex(0)
        elif dtype == "S":
            w.ui.cbTD_Type.setCurrentIndex(1)
        # ReadDetector(chan)
        w.ui.ckbTD_Set.setCheckState(2)
        w.ui.lblTD_Type.setText(str(TD_Type).strip("[]"))
        # ReadDetectors()
    else:
        w.ui.cbTD_Type.setCurrentIndex(0)
        w.ui.ckbTD_Set.setCheckState(0)
        TD_State[chan] = ' '
    ReadDetectors()

def setTD_Settings():
    chan = w.ui.sbTD_Chan.value()-1
    if w.ui.ckbTD_Set.checkState() == 2:
        TD_Type[chan] = w.ui.cbTD_Type.currentText()[0]
    else:
        TD_Type[chan] = ' '
    w.ui.lblTD_Type.setText(str(TD_Type).strip("[]"))
    TestIfModified()
    showTD_Settings()

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
    ttype = w.ui.cbTS_Type.currentText()[0]
    chan = w.ui.sbSL_Chan.value()-1
    # TS_State[chan] = TS_Off
    # TS_Type[chan] = ttype

    if ttype == "S":
        w.ui.gbxSignal.setDisabled(False) 
    elif ttype == "B":
        w.ui.gbxBoom.setDisabled(False)
    elif ttype == "F":
        w.ui.gbxFacility.setDisabled(False)
    w.ui.lblTS_Type.setText(str(TS_Type).strip("[]"))
    w.ui.lblTS_State.setText(str(TS_State).strip("[]"))
    TestIfModified()
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
        w.ui.ckbSL_Set.setCheckState(2)
    else:
        TS_Type[chan] = " "
        TS_State[chan] = TS_Off
    w.ui.lblTS_Type.setText(str(TS_Type).strip("[]"))
    TestIfModified()
    showTS_Settings()

def showTS_Settings():
    chan = w.ui.sbSL_Chan.value()-1
    ttype = TS_Type[chan]        # w.ui.cbTS_Type.currentText()[0]
    if ttype != " ":
        if ttype == "S":
            w.ui.cbTS_Type.setCurrentIndex(0) 
        elif ttype == "B":
            w.ui.cbTS_Type.setCurrentIndex(1)
        elif ttype == "F":
            w.ui.cbTS_Type.setCurrentIndex(2)
        w.ui.ckbSL_Set.setCheckState(2)
    else:
        # w.ui.cbTS_Type.setCurrentIndex(0) 
        TS_State[chan] = TS_Off
        w.ui.ckbSL_Set.setCheckState(0)
        w.ui.rbSF_Left .setPalette(palBlk)
        w.ui.rbSF_Right .setPalette(palBlk)
        w.ui.rbSB_Left .setPalette(palBlk)
        w.ui.rbSB_Right.setPalette(palBlk)
        w.ui.rbSL_Top .setPalette(palBlk)
        w.ui.rbSL_Bottom.setPalette(palBlk)
        w.ui.lblTD_State.setText(str(TD_State).strip("[]"))
    w.ui.lblTS_State.setText(str(TS_State).strip("[]"))

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

def clearSV():
        drawSV("M","b")
        drawSV("L","b")
        drawSV("R","b")
        drawSV("B","b")
        drawSV("D","b")

def setSWType():
#     showSV_Settings()
    swType = w.ui.cbSw_Type.currentText()[0]
    chan = w.ui.sbSw_Chan.value()-1
    if swType == "B":
        w.ui.rbSw_M.setText("Up")
    else:
        w.ui.rbSw_M.setText("Main")

def showSV_Settings():
    chan = w.ui.sbSw_Chan.value()-1
    stype = SV_Type[chan]     # w.ui.cbSw_Type.currentText()[0]
    if stype != " ":
        w.ui.ckbSW_Set.setCheckState(2)
    else:
        w.ui.ckbSW_Set.setCheckState(0)

    sstate = SV_State[chan]
    # w.ui.rbSw_M.setText("Main")
    if stype != " ":
        if stype == "R":
            w.ui.cbSw_Type.setCurrentIndex(0) 
        elif stype == "L":
            w.ui.cbSw_Type.setCurrentIndex(1)
        elif stype == "W":
            w.ui.cbSw_Type.setCurrentIndex(2)
        elif stype == "B":
            w.ui.cbSw_Type.setCurrentIndex(3)
            # w.ui.rbSw_M.setText("Up")
        w.ui.lblSV_Type.setText(str(SV_Type).strip("[]"))
        if sstate != " ":
            if sstate == "M":
                if w.ui.rbSw_M.isChecked() == False:
                    w.ui.rbSw_M.toggle()
                SetForMain()
            elif sstate == "S":
                if w.ui.rbSw_Spur.isChecked() == False:     # SetForSpur()
                    w.ui.rbSw_Spur.toggle()
                SetForSpur()
            elif sstate == "U":
                if w.ui.rbSw_M.isChecked() == False:
                    w.ui.rbSw_M.toggle()
                SetForMain()
            else:               # if sstate == "D":
                if w.ui.rbSw_Down.isChecked() == False:
                    w.ui.rbSw_Down.toggle()
                SetForDown()
            # w.ui.ckbSW_Set.setCheckState(2)
    else:
        # w.ui.cbSw_Type.setCurrentIndex(0) 
        if w.ui.cbSw_Type.currentText()[0] == "B":
            w.ui.rbSw_M.setText("Up")
        # Clear check states
        if w.ui.rbSw_M.isChecked() == False:
            w.ui.rbSw_M.toggle()
        # show setup for Main    
        w.ui.cbSw_Type.setCurrentIndex(0)
        clearSV()
        drawSV("M","B")
        # drawSV("L","b")
        # drawSV("R","b")
        w.ui.ckbSW_Set.setCheckState(0)

def setSV_Settings():
    chan = w.ui.sbSw_Chan.value()-1
    if w.ui.ckbSW_Set.checkState() == 2:
        SV_Type[chan] = w.ui.cbSw_Type.currentText()[0]
    else:
        SV_Type[chan] = " "
    w.ui.lblSV_Type.setText(str(SV_Type).strip("[]"))
    TestIfModified()
    showSV_Settings()

def SetForMain():
    stype =  w.ui.cbSw_Type.currentText()[0]
    clearSV()
    # drawSV("M","b")
    # drawSV("L","b")
    # drawSV("R","b")
    # drawSV("B","b")
    # drawSV("D","b")
    if stype == "W":
        Servo_Control(w.ui.sbSw_Chan.value()-1,SW_Main,stype)
        # drawSV("M","b")
        drawSV("L","B")
        #drawSV("R","b")
    else:
        if stype == "B":
            Servo_Control(w.ui.sbSw_Chan.value()-1,BM_Up,stype)
        else:
            Servo_Control(w.ui.sbSw_Chan.value()-1,SW_Main,stype)
        drawSV("M","B")
        # drawSV("L","b")
        # drawSV("R","b")
    # drawSV("D","b")
    w.ui.lblSV_State.setText(str(SV_State).strip("[]"))
    # showSV_Settings()

def SetForSpur():
    stype = w.ui.cbSw_Type.currentText()[0]
    if stype != "B":
        Servo_Control(w.ui.sbSw_Chan.value()-1,SW_Spur, stype)
        clearSV()
        if stype == "L":
            drawSV("L","B")
        elif stype == "R":
            drawSV("R","B")
        elif stype == "W":
            drawSV("L","b")
            drawSV("R","B")
        w.ui.lblSV_State.setText(str(SV_State).strip("[]"))
        # showSV_Settings()

def SetForDown():
    stype = w.ui.cbSw_Type.currentText()[0]
    if stype == "B":
        Servo_Control(w.ui.sbSw_Chan.value()-1,BM_Down, stype)
        clearSV()
        # drawSV("M","b")
        drawSV("D","B")
        w.ui.lblSV_State.setText(str(SV_State).strip("[]"))
        # showSV_Settings()

def enSwitches():
    gbxSwitches.setEnabled(True)

# Generate a List of Files with (extension)
def GenFileList(ext):
    #FileList = []
    FileList = os.listdir("./")
    # search for files with "ext"
    fList = []
    for i in range(len(FileList)-1):
        if FileList[i].count(ext):
            fList.append(FileList[i])
    return(fList)

def LoadTrkInv():
    global TrackInventory
    Load_Track_Inventory(TrackInventory)
    w.ui.lblFile.setText(TrackInventory)

def SaveTrkInv():
    global TrackInventory
    Save_Track_Inventory(TrackInventory)
    Load_Track_Inventory(TrackInventory)

class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_mwTester()
        self.ui.setupUi(self)

        # self.ui.lblFile.setText(TrackInventory)

        self.ui.lblBds_Avail.setText(BdsAvailable)

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
        self.ui.frame_1.setPalette(palGray)
        self.ui.frame_2.setPalette(palGray)
        self.ui.frame_3.setPalette(palGray)
        self.ui.frame_4.setPalette(palGray)

        def FileOpen(SorO):
            global TrackInventory

            FList = []
            dlgwin = QDialog()
            if SorO == "S":
                dlg = Ui_dlgFileSave()
            else:
                dlg = Ui_dlgFileOpen()
            dlg.setupUi(dlgwin)
            FList = GenFileList(".txt")
            dlg.cbxFileList.addItems(FList)
            if dlgwin.exec_():
                TrackInventory = dlg.cbxFileList.currentText()
                if SorO == "O":
                    Load_Track_Inventory(TrackInventory)
                else:
                    Save_Track_Inventory(TrackInventory)

        def SaveTrkInvAs():
            FileOpen("S")

        def LoadTrkInvAs():
            FileOpen("O")

        def CloseConfigurator():
            global TrackInventory
            
#            Save_Train_Inventory()
            self.close()

        # self.ui.actionSelect_File.triggered.connect(FileOpen("O"))   
        self.ui.actionOpen_Inventory.triggered.connect(LoadTrkInv)
        self.ui.actionOpen_Inventory_As.triggered.connect(LoadTrkInvAs)
        self.ui.actionSave_Inventory.triggered.connect(SaveTrkInv)
        self.ui.actionSave_Inventory_As.triggered.connect(SaveTrkInvAs)
        self.ui.actionExit.triggered.connect(CloseConfigurator)

        self.ui.ckbSW_Set.clicked.connect(setSV_Settings)
        self.ui.cbSw_Type.currentTextChanged.connect(setSWType)
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
        # self.ui.gbxSwitches.clicked.connect(enSwitches)


        self.TTimer = QTimer()
        self.TTimer.timeout.connect(TS_Blinker)
        self.TTimer.start(50)

        self.DTimer = QTimer()
        self.DTimer.timeout.connect(ReadDetectors)
        if IOPI_Full >= 1:
            self.DTimer.start(100)
        else:
            self.DTimer.start(1000)

app = QApplication(sys.argv)
w = AppWindow()
w.show()
#w.move(1984,0)
sys.exit(app.exec_())
