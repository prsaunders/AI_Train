# from math import fabs
# from operator import lt
import os
import sys

# from PyQt5 import QtWidgets, QtCore, QtGui
# # from PyQt5 import qtbluetooth as QtBt
from PyQt5.QtGui import QPalette, QColor, QFont    #, QTextBlock
from PyQt5.QtWidgets import QApplication, QMainWindow   #, QLabel, QGridLayout, QFormLayout, QTableWidgetItem
# rom PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QDialog # , QTextEdit, QListView, QListWidget
# from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt # , QEvent, QFileSelector, QTimerEvent

from IOPi import IOPi
# import RPi.GPIO as GPIO
# import threading
from time import sleep, time, ctime  # , time
from adafruit_servokit import ServoKit
# from psutil import cpu_times_percent

#from Train_Hardware_Test_and_Setup import Save_Train_Inventory

kit = ServoKit(channels=16)
# # from adafruit_servokit import PCA9685

# from datetime import datetime

from AI_Win import Ui_mwinAI_Train
from Acela_Strt_Pt import Ui_dlgAcelaStPt
from CT_Shore_Strt_Pt import Ui_dlgCTStPt
from FileOpen import Ui_dlgFileOpen
# from FileSave import Ui_dlgFileSave

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

# global SV_Type, BM_State, TD_State, TS_Type

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
TD_State = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
TD_DBnc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
TS_Type = ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "B", " ", " ", " ", " ", " "]
#global TS_State:   (see above) 
TS_State = ["R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "R", "O", "O", "O", "O", "O", "O"]
TS_Ind = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#global TS_Time
TS_Time = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

TS_Chan = 0

# Train Layout Data Max values
ServoCT = 16        # Channels 1 to 16  (16 max)
TrainDET = 16       # Detectors 1 to 16 (16 max)
TrainSIG = 8        # Signals 1 to 8    (8 max) More reqires another IO_Pi Bd + Plus Interface Bd CHG

# train MACs
greentrain = '90:84:2B:BE:F5:DD'
yellowtrain = '90:84:28:22:FC:3F'
loneranger = '90:84:2B:0C:22:02'

# Local and Main Stations and Mileage Info
Main_NS = ['North Yard',
           'Boston, MA(BBY)', 'Route 128, MA(RTE)', 'Providence, RI(PVD)', 'New Haven, CT(NHV)',
           'Stamford, CT(STM)', 'New York, NY(NYP)', 'Newark, NJ(NWK)', 'Philadelphia, PA(PHL)',
           'Wilmington, DE(WIL)', 'Baltimore, MD(BAL)', 'BWI Marshall Airport, MD(BWI)', 'Washington, DC(WAS)',
           'South Yard']
Main_M_NS = [0, 10, 30, 100, 40, 40, 10, 80, 30, 70, 10, 30, 0]
Main_M_SN = [0, 30, 10, 70, 30, 80, 10, 40, 40, 100, 30, 10, 0]
mTtl_Dn = [450, 450, 440, 410, 310, 270, 230, 220, 140, 110, 40, 30,0, 0]
mTtl_Up = [0, 0, 10, 40, 140, 180, 220, 230, 310, 340, 410, 420, 450, 450]
# mTtl_Dn = [446, 446, 436, 403, 302, 261, 226, 216, 135, 107, 40, 31, 0, 0]
# mTtl_Up = [0, 0, 10, 43, 144, 185, 220, 230, 311, 339, 406, 415, 446, 446]
Main_Dir = 'S'      # S = Moving South, N = Moving North
MT_Pos = ""
MScale = 10          # miles/loop
MainStation = ""
MainMiles = int(0)  # MTrip[0,0]
mMilesToNext = 0.0  # MTrip[1,0]
mTripMiles = 0.0    # MtoSta[0.0]
mToStnMiles = 0.0   # MtoSta[1,0]
mDetMiles = 0.0
mExpress = False

mPtr = int(0)
# mSNPtr = int(0)
mToSta = False
mAtSta = False
mLvgSta = False

Local_NS = ['North Yard(S)',
            'New London(S)', 'Old Saybrook(S)', 'Westbrook(S)', 'Guilford(S)',
            'Branford(S)', 'State Street(S)', 'New Haven(S)', 'West Haven(M)',
            'Milford(M)', 'Stratford(M)', 'Bridgeport(M)', 'Fairfield Metro(M)',
            'Fairfield(M)', 'Westport(M)', 'South Norwalk(M)', 'Darien(M)', 
            'Stamford(M)', 'South Yard(M)']
Loc_M_NS = [0, 18, 5, 14, 9, 11, 1, 3, 7, 5, 4, 4, 2, 7, 3, 4, 5, 0]
Loc_M_SN = [0, 5, 4, 3, 7, 2, 4, 4, 5, 7, 3, 1, 11, 9, 14, 5, 18, 0]
lTtl_Dn = [102, 102, 84, 79, 65, 56, 45, 44, 41, 34, 29, 25, 21, 19, 12, 9, 5, 0, 0]
lTtl_Up = [0, 0, 18, 23, 37, 46, 57, 58, 61, 68, 73, 77, 81, 83, 90, 93, 97, 102, 102]
NLine = "Shore Line East"
SLine = "Metro North"
Local_Dir = 'S'     # S = Moving South, N = Moving North
LT_Pos = ""
LScale = 1          # miles/loop
LocalStation = ""
LocalMiles = int(0) # LTrip[0,0]
lMilesToNext = 0.0  # LTrip[1,0]    Sub from
lTripMiles = 0.0    # LtoSta[0,0]   Add to
lToStnMiles = 0.0   # LtoSta[1,0]   Add to
lDetMiles = 0.0
lExpress = False

lPtr = int(0)
# lSNPtr = int(0)

lToSta = False  
lAtSta = False
lLeavingSta = False
lToSiding = False

oneMin = 600            # 1 Minute
fiveMin = 3000          # 5 Minutes,  use at New Haven and New York for change of track
staDelay = oneMin 

trackMileScale = 200/12/5280
timeMD = ""
timeM = [0.0, 0.0, 0.0, 0.0]
timeMPre = [0.0, 0.0, 0.0, 0.0]
timeMDir = ""
mainSpd = 0.0
timeLD = ""
timeL = [0.0, 0.0, 0.0, 0.0]
timeLPre = [0.0, 0.0, 0.0, 0.0]
timeLDir = ""
localSpd = 0.0

# Sidings and Main to Local Flags
yLeft1 = False
yLeft2 = False
yRight = False
MoverL = False
MLswitch = False
lsiding = False
mTurnAround = False
mTurned = False
lTurnAround = False
lTurned = False

lp1 = False         # ignore detectors for 1 loop
lpCtr = int(0)
ctLps = False

SessionName = "CurSession"

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
palBlack = QPalette()
palBlack.setColor(QPalette.WindowText, Qt.black)
palRedTxt = QPalette()
palRedTxt.setColor(QPalette.WindowText, Qt.red)
palBlnk = QPalette()
palBlnk.setColor(QPalette.WindowText, QColor(237,237,237))
palAtSta = QPalette()
palAtSta.setColor(QPalette.Button, Qt.cyan)
palAwaySta = QPalette()
palAwaySta.setColor(QPalette.Button, Qt.darkCyan)  #QColor(85,170,255))


Testing = False
RunDets = 0

# For use with Scope to see timing
# TimeTst = True
# if TimeTst:
#     TrnSigW.write_pin(15,0)
# if TimeTst:
#     TrnSigW.write_pin(15,1)
# if TimeTst:
#     TrnSigW.write_pin(16, 0)
# if TimeTst:
#     TrnSigW.write_pin(16, 0)

def TS_Blinker():
    global TS_Type, TS_State, TS_Time, TS_Ind
    
    for i in range(len(TS_State)):
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
        if i < 8:
            pin = ((i*2)+1)
            TS = TrnSigM
        elif i < 16:
            pin = (((i-8)*2)+1)
            TS = TrnSigL
        else:
            pin = (((i-16)*2)+1)
            TS = TrnSigW
 
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
        elif TS_State[i] == TS_O1:
            TS.write_pin(pin, 0)
            TS.write_pin(pin+1,1)
        elif TS_State[i] == TS_O2:
            TS.write_pin(pin, 1)
            TS.write_pin(pin+1,0)

def Turn_Around(dir):
    global TS_State, yLeft1, yRight

    if yLeft1==False or yRight==False:
        # Okay to use Wyes as Siding for Local Train
        if dir == "S":
            TS_State[10] = TS_Yellow
            Set_Switches("L", "S")
        else:
            TS_State[14] = TS_Yellow
            Set_Switches("L", "N")

        if yLeft1 == False:
            Set_Switches("Y", "L")
        else:
            Set_Switches("Y", "R")
    if yLeft1==False or yRight==False:
        # Okay to use Wyes as Siding for Local Train
        if dir == "S":
            TS_State[10] = TS_Yellow
            Set_Switches("L", "S")
        else:
            TS_State[14] = TS_Yellow
            Set_Switches("L", "N")

def SetLocToMain():
    # Set Local back to Main
    Set_Switches("L", "M")
    # MAIN LINE LIGHTS FOR WHEN DOUBLE CROSSOVER IN PLAY
    # TS_State[0] = TS_Yellow
    # TS_State[4] = TS_Red
    # w.ui.pbMSS_1.setPalette(palYellow)
    # w.ui.pbMSN_1.setPalette(palRed)
    TS_State[8] = TS_Yellow
    TS_State[12] = TS_Red
    w.ui.pbLSS_1.setPalette(palYellow)
    w.ui.pbLSN_1.setPalette(palRed)
    TS_State[18] = TS_Red
    w.ui.pbWyeLSO.setPalette(palRed)
    w.ui.pbWyeRSO.setPalette(palRed)

def setSpdDir(l, n, t):
    global  timeMDir, timeMD, timeMPre, timeM, timeLDir, timeLD, timeLPre, timeL, \
            mainSpd, localSpd, Main_Dir, Local_Dir

    n1 = ((n-1)%4)
    n2 = ((n+1)%4)
    if l == "M":
        timeMPre[n] = t
        if timeMD == n1:
            timeM[n] = t - timeMPre[n1]
            timeMDir = "S"
        elif timeMD == n2:
            timeM[n] = t - timeMPre[n2]
            timeMDir = "N"
        timeMD = n
        if timeM[n] != 0:
            mainSpd = 128.56*(timeM[n]*MScale)**-1.422
            if timeMDir != Main_Dir:
                mainSpd *= -1
        else:
            mainSpd = 0.0
        # display  Main Speeds
        w.ui.mSpd.setText(str("%.1f" % mainSpd) + " " + timeMDir)
        if Main_Dir != timeMDir:
            w.ui.mSpd.setPalette(palRedTxt)
        else:
            w.ui.mSpd.setPalette(palBlack)
    else:
        timeLPre[n] = t
        if timeLD == n1:
            timeL[n] = t - timeLPre[n1]
            timeLDir = "S"
        elif timeLD == n2:
            timeL[n] = t - timeLPre[n2]
            timeLDir = "N"
        timeLD = n
        if timeL[n] != 0:
            localSpd = 198.12*timeL[n]**-1.588
        else:
            localSpd = 0.0
        # display Local Speeds
        w.ui.lSpd.setText(str("%.1f" % localSpd) + " " + timeLDir)
        if Local_Dir != timeLDir:
            w.ui.lSpd.setPalette(palRedTxt)
        else:
            w.ui.lSpd.setPalette(palBlack)


def ReadDetectors():
    global  TD_Type, TD_State, mPtr, lPtr, Main_Dir, mTurnAround, Local_Dir, \
            MainMiles, LocalMiles, mToStnMiles, lToStnMiles, mTripMiles, TS_State, \
            lTripMiles, mMilesToNext, lMilesToNext, mLvgSta,  mDetMiles, lDetMiles, \
            Testing, MT_Pos, LT_Pos, RunDets, mToSta, mAtSta, lpCtr, ctLps, \
            lToSta, lAtSta, yLeft1, yLeft2, yRight, lp1, MoverL, lsiding, lTurnAround, \
            MLswitch, mTurned, lTurned, staDelay, oneMin, fiveMin, lToSiding,  \
            timeMDir, timeMD, timeMPre, timeM, timeLDir, timeLD, timeLPre, timeL    # , Set_Switches
               
    if RunDets != 0:
        det = 0
        for i in range(len(TD_Type)):
            lohi = False
            hilo = False
            det = TrnDet.read_pin(i+1)
            if det != TD_State[i] and TD_DBnc[i] == 0:
                TD_State[i] = det
                if det == 1:
                    lohi = True
                    TD_DBnc[i] = 1
                else:
                    hilo = True
                if TD_Type[i] == "D":
                    if i < 4 and RunDets != 2:
                        # Main Loop
                        MT_Pos = (str(i)+Main_Dir)
                        if i == 0:
                            if TD_State[i]:
                                w.ui.pbMD_1.setPalette(palBlue)
                                if Testing == False:
                                    if Main_Dir == "S":
                                        TS_State[0] = TS_Green
                                        w.ui.pbMSS_1.setPalette(palGreen)
                                        TS_State[1] = TS_Green
                                        TS_State[2] = TS_Yellow
                                        TS_State[3] = TS_Red
                                        w.ui.pbMSS_2.setPalette(palGreen)
                                        w.ui.pbMSS_3.setPalette(palYellow)
                                        w.ui.pbMSS_4.setPalette(palRed)
                                    else:       # == "N"
                                        TS_State[4] = TS_Red
                                        TS_State[5] = TS_Yellow
                                        TS_State[6] = TS_Green
                                        TS_State[7] = TS_Green
                                        w.ui.pbMSN_1.setPalette(palRed)
                                        w.ui.pbMSN_2.setPalette(palYellow)
                                        w.ui.pbMSN_3.setPalette(palGreen)
                                        w.ui.pbMSN_4.setPalette(palGreen)
                                if lohi:
                                    # use for speed and direction detection
                                    setSpdDir("M", i, time())
                            else:
                                w.ui.pbMD_1.setPalette(palBlank)
                                if lp1:
                                    if MoverL and mLvgSta and (Main_Dir == "N"):           #  and mToSta == False:
                                        if hilo:
                                            # return main sw to MAIN
                                            Set_Switches("M", "M")
                                            # Return Local so it can come back onto Local Loop
                                            if Local_Dir == "S":
                                                TS_State[10] = TS_Yellow
                                                Set_Switches("L", "S")
                                            else:
                                                TS_State[14] = TS_Yellow
                                                Set_Switches("L", "N")
                                            TS_State[18] = TS_Yellow
                                            w.ui.pbWyeLSO.setPalette(palYellow)
                                            w.ui.pbWyeRSO.setPalette(palYellow)
                                            MoverL = False
                                            mLvgSta = False
                        elif i == 1:
                            if TD_State[i]:
                                w.ui.pbMD_2.setPalette(palBlue)
                                if Testing == False:
                                    if Main_Dir == "S":
                                        TS_State[0] = TS_Red
                                        TS_State[1] = TS_Green
                                        TS_State[2] = TS_Green
                                        TS_State[3] = TS_Yellow
                                        w.ui.pbMSS_1.setPalette(palRed)
                                        w.ui.pbMSS_2.setPalette(palGreen)
                                        w.ui.pbMSS_3.setPalette(palGreen)
                                        w.ui.pbMSS_4.setPalette(palYellow)
                                    else:       # == "N"
                                        TS_State[4] = TS_Green
                                        TS_State[5] = TS_Red
                                        TS_State[6] = TS_Yellow
                                        TS_State[7] = TS_Green
                                        w.ui.pbMSN_1.setPalette(palGreen)
                                        w.ui.pbMSN_2.setPalette(palRed)
                                        w.ui.pbMSN_3.setPalette(palYellow)
                                        w.ui.pbMSN_4.setPalette(palGreen)
                                if lohi:
                                    # use for speed and direction detection
                                    setSpdDir("M", i, time())
                            else:
                                w.ui.pbMD_2.setPalette(palBlank)
                                if lp1:
                                    if MoverL and mLvgSta and (Main_Dir == "S"):
                                        if hilo:
                                            # return main sw to MAIN
                                            Set_Switches("M", "M")
                                            # Return Local so it can come back onto Local Loop
                                            if Local_Dir == "S":
                                                TS_State[10] = TS_Yellow
                                                Set_Switches("L", "S")
                                            else:
                                                TS_State[14] = TS_Yellow
                                                Set_Switches("L", "N")
                                            TS_State[18] = TS_Yellow
                                            w.ui.pbWyeLSO.setPalette(palYellow)
                                            w.ui.pbWyeRSO.setPalette(palYellow)
                                            MoverL = False
                                            mLvgSta = False
                        elif i == 2:
                            if TD_State[i]:
                                w.ui.pbMD_3.setPalette(palBlue)
                                if Testing == False:
                                    if Main_Dir == "S":
                                        TS_State[0] = TS_Yellow
                                        TS_State[1] = TS_Red
                                        TS_State[2] = TS_Green
                                        TS_State[3] = TS_Green
                                        w.ui.pbMSS_1.setPalette(palYellow)
                                        w.ui.pbMSS_2.setPalette(palRed)
                                        w.ui.pbMSS_3.setPalette(palGreen)
                                        w.ui.pbMSS_4.setPalette(palGreen)
                                    else:       # == "N"
                                        TS_State[4] = TS_Green
                                        TS_State[5] = TS_Green
                                        TS_State[6] = TS_Red
                                        TS_State[7] = TS_Yellow
                                        w.ui.pbMSN_1.setPalette(palGreen)
                                        w.ui.pbMSN_2.setPalette(palGreen)
                                        w.ui.pbMSN_3.setPalette(palRed)
                                        w.ui.pbMSN_4.setPalette(palYellow)
                                if lohi:
                                    # use for speed and direction detection
                                    setSpdDir("M", i, time())
                            else:
                                w.ui.pbMD_3.setPalette(palBlank)
                        elif i == 3:
                            if TD_State[i]:
                                w.ui.pbMD_4.setPalette(palBlue)
                                if Testing == False:
                                    if Main_Dir == "S":
                                        TS_State[0] = TS_Green
                                        TS_State[1] = TS_Yellow
                                        TS_State[2] = TS_Red
                                        TS_State[3] = TS_Green
                                        w.ui.pbMSS_1.setPalette(palGreen)
                                        w.ui.pbMSS_2.setPalette(palYellow)
                                        w.ui.pbMSS_3.setPalette(palRed)
                                        w.ui.pbMSS_4.setPalette(palGreen)
                                    else:       # == "N"
                                        TS_State[4] = TS_Yellow
                                        TS_State[5] = TS_Green
                                        TS_State[6] = TS_Green
                                        TS_State[7] = TS_Red
                                        w.ui.pbMSN_1.setPalette(palYellow)
                                        w.ui.pbMSN_2.setPalette(palGreen)
                                        w.ui.pbMSN_3.setPalette(palGreen)
                                        w.ui.pbMSN_4.setPalette(palRed)
                                if lohi:
                                    # use for speed and direction detection
                                    setSpdDir("M", i, time())
                            else:
                                w.ui.pbMD_4.setPalette(palBlank)
                        if lohi:
                            # Main Loop Mileage
                            if lp1:
                                if mToSta == False:  # if MoverL == False:      #  and mToSta == False:
                                    if (mPtr != 0 and mPtr != len(Main_NS)):
                                        mToStnMiles -= mDetMiles
                                        mTripMiles += mDetMiles
                                        mMilesToNext -= mDetMiles
                                        displayMainMiles()
                                if (mToStnMiles < MScale) and (mToSta == False):   #  and (MoverL == False):
                                    # MAIN needs to go to the station, give Local chance to go into siding
                                    if yLeft1==False or yRight==False:
                                        # Okay to use Wyes as Siding for Local Train
                                        MoverL = True
                                        mToSta = True
                                        if Main_Dir == "S":
                                            TS_State[0] = TS_Red
                                        else:
                                            TS_State[4] = TS_Red

                                        if Local_Dir == "S":
                                            TS_State[10] = TS_Yellow
                                            Set_Switches("L", "S")
                                        else:
                                            TS_State[14] = TS_Yellow
                                            Set_Switches("L", "N")

                                        if yLeft1 == False:
                                            Set_Switches("Y", "L")
                                        else:
                                            Set_Switches("Y", "R")

                                        TS_State[18] = TS_Red
                                        w.ui.pbWyeLSO.setPalette(palRed)
                                        w.ui.pbWyeRSO.setPalette(palRed)

                                        lToSiding = True
                                        # set local lights of travel to yellow
                                        
                                        # wait for local to go into turn off
                                        # Look for Det 8/9 or 10 to go true
                                    else:
                                        # Main and Local change loops
                                        MLswitch = True

                                        if ((MT_Pos == "3N") or (MT_Pos == "2S")) and (mToStnMiles <= mDetMiles):
                                            # Ready to head to station on inner Loop
                                            w.ui.lblMain_Arriv.text = "Arriving"
                                            TS_State[21]=TS_On      # turn on station lights

                                            # time to set switches and signals to allow 
                                            # MAIN and LOCAL to switch LOOPs
                                            if Local_Dir == Main_Dir:
                                                if (LT_Pos == "3N" and Main_Dir == "N"):
                                                    TS_State[4] = TS_Yellow
                                                    TS_State[5] = TS_Yellow
                                                    TS_State[13] = TS_Red
                                                elif (LT_Pos == "2S" and Main_Dir == "S"):
                                                    TS_State[3] = TS_Yellow
                                                    TS_State[0] = TS_Yellow
                                                    TS_State[11] = TS_Red
                                                else:
                                                    TS_State[0] = TS_Red
                                                    TS_State[3] = TS_Red
                                if MoverL and mToSta and lsiding:
                                    TS_State[21]=TS_On      # turn on station light
                            if MoverL and mToSta:
                                if lsiding:
                                    if Main_Dir == "S":
                                        TS_State[0] = TS_Yellow
                                        w.ui.pbMSS_1.setPalette(palYellow)
                                    else:
                                        TS_State[4] = TS_Yellow
                                        w.ui.pbMSN_1.setPalette(palYellow)
                                else:
                                    if Main_Dir == "S":
                                        TS_State[0] = TS_Red
                                        w.ui.pbMSS_1.setPalette(palRed)
                                    else:
                                        TS_State[4] = TS_Red
                                        w.ui.pbMSN_1.setPalette(palRed)
                    elif i < 8 and RunDets != 1:
                        # Local Loop
                        LT_Pos = (str(i-4)+Local_Dir)
                        if i == 4:
                            if TD_State[i]:
                                w.ui.pbLD_1.setPalette(palBlue)
                                if Testing == False:
                                    if MoverL and lsiding:
                                        if Main_Dir == "S":
                                            TS_State[11] = TS_Red
                                            TS_State[10] = TS_Yellow
                                            TS_State[9] = TS_Yellow
                                            TS_State[8] = TS_Yellow
                                            w.ui.pbLSS_1.setPalette(palYellow)
                                            w.ui.pbLSS_2.setPalette(palYellow)
                                            w.ui.pbLSS_3.setPalette(palYellow)
                                            w.ui.pbLSS_4.setPalette(palRed)
                                        else:       # == "N"
                                            TS_State[15] = TS_Yellow
                                            TS_State[14] = TS_Yellow
                                            w.ui.pbLSN_3.setPalette(palYellow)
                                            w.ui.pbLSN_4.setPalette(palYellow)
                                            TS_State[13] = TS_Yellow
                                            TS_State[12] = TS_Red
                                            w.ui.pbLSN_1.setPalette(palRed)
                                            w.ui.pbLSN_2.setPalette(palYellow)
                                    else:
                                        if Local_Dir == "S":
                                            TS_State[11] = TS_Red
                                            TS_State[10] = TS_Yellow
                                            if lToSta:
                                                TS_State[9] = TS_Yellow
                                                TS_State[8] = TS_Yellow
                                                w.ui.pbLSS_1.setPalette(palYellow)
                                                w.ui.pbLSS_2.setPalette(palYellow)
                                            else:
                                                TS_State[9] = TS_Green
                                                TS_State[8] = TS_Green
                                                w.ui.pbLSS_1.setPalette(palGreen)
                                                w.ui.pbLSS_2.setPalette(palGreen)
                                            w.ui.pbLSS_3.setPalette(palYellow)
                                            w.ui.pbLSS_4.setPalette(palRed)
                                        else:       # == "N"
                                            if lToSta:
                                                TS_State[15] = TS_Yellow
                                                TS_State[14] = TS_Yellow
                                                w.ui.pbLSN_3.setPalette(palYellow)
                                                w.ui.pbLSN_4.setPalette(palYellow)
                                            else:
                                                TS_State[15] = TS_Green
                                                TS_State[14] = TS_Green
                                                w.ui.pbLSN_3.setPalette(palGreen)
                                                w.ui.pbLSN_4.setPalette(palGreen)
                                            TS_State[13] = TS_Yellow
                                            TS_State[12] = TS_Red
                                            w.ui.pbLSN_1.setPalette(palRed)
                                            w.ui.pbLSN_2.setPalette(palYellow)
                                if lohi:
                                    # use for speed and direction detection
                                    setSpdDir("L", i-4, time())
                            else:
                                w.ui.pbLD_1.setPalette(palBlank)
                        elif i == 5:
                            if TD_State[i]:
                                w.ui.pbLD_2.setPalette(palBlue)
                                if Testing == False:
                                    if MoverL and lsiding:
                                        if Main_Dir == "S":
                                            TS_State[8] = TS_Red
                                            TS_State[9] = TS_Yellow
                                            TS_State[10] = TS_Yellow
                                            w.ui.pbLSS_2.setPalette(palYellow)
                                            w.ui.pbLSS_3.setPalette(palYellow)
                                            TS_State[11] = TS_Yellow
                                            w.ui.pbLSS_1.setPalette(palRed)
                                            w.ui.pbLSS_4.setPalette(palYellow)
                                        else:       # == "N"
                                            TS_State[12] = TS_Yellow
                                            TS_State[15] = TS_Yellow
                                            w.ui.pbLSN_1.setPalette(palYellow)
                                            w.ui.pbLSN_4.setPalette(palYellow)
                                            TS_State[13] = TS_Red
                                            TS_State[14] = TS_Yellow
                                            w.ui.pbLSN_2.setPalette(palRed)
                                            w.ui.pbLSN_3.setPalette(palYellow)
                                    else:
                                        if Local_Dir == "S":
                                            TS_State[8] = TS_Red
                                            if lToSta:
                                                TS_State[9] = TS_Yellow
                                                TS_State[10] = TS_Yellow
                                                w.ui.pbLSS_2.setPalette(palYellow)
                                                w.ui.pbLSS_3.setPalette(palYellow)
                                            else:
                                                TS_State[9] = TS_Green
                                                TS_State[10] = TS_Green
                                                w.ui.pbLSS_2.setPalette(palGreen)
                                                w.ui.pbLSS_3.setPalette(palGreen)
                                            TS_State[11] = TS_Yellow
                                            w.ui.pbLSS_1.setPalette(palRed)
                                            w.ui.pbLSS_4.setPalette(palYellow)
                                        else:       # == "N"
                                            if lToSta:
                                                TS_State[12] = TS_Yellow
                                                TS_State[15] = TS_Yellow
                                                w.ui.pbLSN_1.setPalette(palYellow)
                                                w.ui.pbLSN_4.setPalette(palYellow)
                                            else:
                                                TS_State[12] = TS_Green
                                                TS_State[15] = TS_Green
                                                w.ui.pbLSN_1.setPalette(palGreen)
                                                w.ui.pbLSN_4.setPalette(palGreen)
                                            TS_State[13] = TS_Red
                                            TS_State[14] = TS_Yellow
                                            w.ui.pbLSN_2.setPalette(palRed)
                                            w.ui.pbLSN_3.setPalette(palYellow)
                                if lohi:
                                    # use for speed and direction detection
                                    setSpdDir("L", i-4, time())
                            else:
                                w.ui.pbLD_2.setPalette(palBlank)
                        elif i == 6:                                                           
                            if TD_State[i]:
                                w.ui.pbLD_3.setPalette(palBlue)
                                if Testing == False:
                                    if MoverL and lsiding:
                                        if Main_Dir == "S":
                                            TS_State[8] = TS_Yellow
                                            TS_State[9] = TS_Red
                                            TS_State[10] = TS_Yellow
                                            TS_State[11] = TS_Yellow
                                            w.ui.pbLSS_1.setPalette(palYellow)
                                            w.ui.pbLSS_2.setPalette(palRed)
                                            w.ui.pbLSS_3.setPalette(palYellow)
                                            w.ui.pbLSS_4.setPalette(palYellow)
                                        else:       # == "N"
                                            TS_State[12] = TS_Yellow
                                            TS_State[13] = TS_Yellow
                                            TS_State[14] = TS_Red
                                            TS_State[15] = TS_Yellow
                                            w.ui.pbLSN_1.setPalette(palYellow)
                                            w.ui.pbLSN_2.setPalette(palYellow)
                                            w.ui.pbLSN_3.setPalette(palRed)
                                            w.ui.pbLSN_4.setPalette(palYellow)
                                    else:
                                        if Local_Dir == "S":
                                            TS_State[8] = TS_Yellow
                                            TS_State[9] = TS_Red
                                            if lToSta:
                                                TS_State[10] = TS_Yellow
                                                TS_State[11] = TS_Yellow
                                            else:
                                                TS_State[10] = TS_Green
                                                TS_State[11] = TS_Green
                                            w.ui.pbLSS_1.setPalette(palYellow)
                                            w.ui.pbLSS_2.setPalette(palRed)
                                            if lToSta:
                                                w.ui.pbLSS_3.setPalette(palYellow)
                                                w.ui.pbLSS_4.setPalette(palYellow)
                                            else:
                                                w.ui.pbLSS_3.setPalette(palGreen)
                                                w.ui.pbLSS_4.setPalette(palGreen)
                                        else:       # == "N"
                                            if lToSta:
                                                TS_State[12] = TS_Yellow
                                                TS_State[13] = TS_Yellow
                                            else:
                                                TS_State[12] = TS_Green
                                                TS_State[13] = TS_Green
                                            TS_State[14] = TS_Red
                                            TS_State[15] = TS_Yellow
                                            if lToSta:
                                                w.ui.pbLSN_1.setPalette(palYellow)
                                                w.ui.pbLSN_2.setPalette(palYellow)
                                            else:
                                                w.ui.pbLSN_1.setPalette(palGreen)
                                                w.ui.pbLSN_2.setPalette(palGreen)
                                            w.ui.pbLSN_3.setPalette(palRed)
                                            w.ui.pbLSN_4.setPalette(palYellow)
                                if lohi:
                                    # use for speed and direction detection
                                    setSpdDir("L", i-4, time())
                            else:
                                w.ui.pbLD_3.setPalette(palBlank)
                                if lp1:
                                    if MoverL == False:
                                        if Local_Dir == "S":
                                            if lsiding:
                                                lsiding = False
                                                # Set Local back to Main
                                                SetLocToMain()
                                                Set_Signals("L","N",TS_Red)
                                        else:                                   # Local_Dir == "N":
                                            if lTurnAround and lTurned == False:
                                                lTurned = True
                                                #lTurnAround = False
                                                # Set Local back to Main
                                                SetLocToMain()
                                                Local_Dir = "S"
                                                Set_Signals("L","N",TS_Red)
                                                lToSta = True
                                                lPtr = 0
                                                # lSNPtr = 16
                                                w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr+1],""))
                                                w.ui.lblLocStaNm.setText(CleanCt(Local_NS[lPtr],""))
                                                w.ui.lblL_L.setText("L")
                                                w.ui.lblL_R.setText("SB")
                        elif i == 7:
                            if TD_State[i]:
                                w.ui.pbLD_4.setPalette(palBlue)
                                if Testing == False:
                                    if MoverL and lsiding:
                                        if Main_Dir == "S":
                                            TS_State[8] = TS_Yellow
                                            TS_State[9] = TS_Yellow
                                            TS_State[10] = TS_Red
                                            TS_State[11] = TS_Yellow
                                            w.ui.pbLSS_1.setPalette(palYellow)
                                            w.ui.pbLSS_2.setPalette(palYellow)
                                            w.ui.pbLSS_3.setPalette(palRed)
                                            w.ui.pbLSS_4.setPalette(palYellow)
                                        else:       # == "N"
                                            TS_State[12] = TS_Yellow
                                            TS_State[13] = TS_Yellow
                                            TS_State[14] = TS_Yellow
                                            TS_State[15] = TS_Red
                                            w.ui.pbLSN_1.setPalette(palYellow)
                                            w.ui.pbLSN_2.setPalette(palYellow)
                                            w.ui.pbLSN_3.setPalette(palYellow)
                                            w.ui.pbLSN_4.setPalette(palRed)
                                    else:
                                        if Local_Dir == "S":
                                            if lToSta:
                                                TS_State[8] = TS_Yellow
                                                TS_State[11] = TS_Yellow
                                                w.ui.pbLSS_1.setPalette(palYellow)
                                                w.ui.pbLSS_4.setPalette(palYellow)
                                            else:
                                                TS_State[8] = TS_Green
                                                TS_State[11] = TS_Green
                                                w.ui.pbLSS_1.setPalette(palGreen)
                                                w.ui.pbLSS_4.setPalette(palGreen)
                                            TS_State[9] = TS_Yellow
                                            TS_State[10] = TS_Red
                                            w.ui.pbLSS_2.setPalette(palYellow)
                                            w.ui.pbLSS_3.setPalette(palRed)
                                        else:       # == "N"
                                            TS_State[12] = TS_Yellow
                                            TS_State[15] = TS_Red
                                            w.ui.pbLSN_1.setPalette(palYellow)
                                            w.ui.pbLSN_4.setPalette(palRed)
                                            if lToSta:
                                                TS_State[13] = TS_Yellow
                                                TS_State[14] = TS_Yellow
                                                w.ui.pbLSN_2.setPalette(palYellow)
                                                w.ui.pbLSN_3.setPalette(palYellow)
                                            else:
                                                TS_State[13] = TS_Green
                                                TS_State[14] = TS_Green
                                                w.ui.pbLSN_2.setPalette(palGreen)
                                                w.ui.pbLSN_3.setPalette(palGreen)
                                if lohi:
                                    # use for speed and direction detection
                                    setSpdDir("L", i-4, time())
                            else:
                                w.ui.pbLD_4.setPalette(palBlank)
                                if lp1:
                                    if MoverL == False:
                                        if Local_Dir == "N":
                                            if lsiding:
                                                lsiding = False
                                                # Set Local back to Main
                                                SetLocToMain()
                                                Set_Signals("L","S",TS_Red)
                                        else:                                       # if Local_Dir == "S":
                                            if lTurnAround and lTurned == False:
                                                lTurned = True
                                                # lTurnAround = False
                                                # Set Local back to Main
                                                SetLocToMain()
                                                Local_Dir = "N"
                                                Set_Signals("L","S",TS_Red)
                                                lToSta = True
                                                lPtr = 18
                                                # lSNPtr = 1
                                                w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr-1],""))
                                                w.ui.lblLocStaNm.setText(CleanCt(Local_NS[lPtr],""))
                                                w.ui.lblL_L.setText("NB")
                                                w.ui.lblL_R.setText("L")
                        # Local Loop Mileage
                        if lohi:
                            if lp1:
                                if (mAtSta == False):
                                    if (lPtr != 0 and lPtr != len(Local_NS)):
                                        lToStnMiles -= lDetMiles
                                        lTripMiles += lDetMiles
                                        lMilesToNext -= lDetMiles
                                        displayLocalMiles()

                                    if (lToStnMiles < LScale):
                                        # Ready to head to station on inner Loop
                                        w.ui.lblLocal_Arriv.setText("Arriving")
                                        lToSta = True
                                        TS_State[21]=TS_On
                                # else:
                                #     if mTurnAround:
                                #         # # Main over Local
                                #         # if (mPtr != 0 and mPtr != len(Main_NS)):
                                #         #     mToStnMiles -= mDetMiles
                                #         #     mTripMiles += mDetMiles
                                #         #     mMilesToNext -= mDetMiles
                                #         #     displayMainMiles()
                                #         # else:
                                #         # MAIN turn-arround
                                #         if Main_Dir == "S":
                                #             mPtr += 1
                                #         else:
                                #             mPtr -= 1
                                #         w.ui.lblMainStaNm.setText(Main_NS[mPtr])
                                #     if (mToStnMiles < MScale):
                                #         # Ready to head to station on inner Loop
                                #         w.ui.lblMain_Arriv.setText("Arriving")
                                #         # set Signal into station to RED
                                #         mToSta = True
                                #         TS_State[21]=TS_On
                    elif i < 12:
                        # Wye Detectors
                        if i == 8:
                            if TD_State[i]:
                                yLeft1 = True
                                w.ui.pbWyeLD_1.setPalette(palBlue)
                                TS_State[17] = TS_Red
                                w.ui.pbWyeLSI.setPalette(palRed)
                                # lower Boom and start flasher
                                Servo_Control(6,"D")
                                TS_State[20] = TS_Yellow
                            else:
                                yLeft1 = False
                                w.ui.pbWyeLD_1.setPalette(palBlank)
                                # raise Boom and stop flasher
                                Servo_Control(6,"U")
                                TS_State[20] = TS_Off
                                if yLeft2 == False:
                                    TS_State[17] = TS_Green
                                    w.ui.pbWyeLSI.setPalette(palGreen)
                                else:
                                    TS_State[17] = TS_Yellow
                                    w.ui.pbWyeLSI.setPalette(palYellow)
                            if MoverL and lToSiding:
                                if lohi:
                                    lsiding = True
                                    lToSiding = False
                                    # Set Local back to Main
                                    Set_Switches("L", "M")
                                    TS_State[18] = TS_Red
                                    w.ui.pbWyeLSO.setPalette(palRed)
                                    w.ui.pbWyeRSO.setPalette(palRed)
                                    # set Main for double-cross
                                    Set_Switches("M", "S")
                                    Set_Switches("M", "N")
                                    if Main_Dir == "S":
                                        TS_State[0] = TS_Yellow
                                        TS_State[4] = TS_Red
                                        w.ui.pbMSS_1.setPalette(palYellow)
                                        w.ui.pbMSN_1.setPalette(palRed)
                                        TS_State[8] = TS_Yellow
                                        TS_State[12] = TS_Red
                                        w.ui.pbLSS_1.setPalette(palYellow)
                                        w.ui.pbLSN_1.setPalette(palRed)
                                    else:
                                        TS_State[0] = TS_Red
                                        TS_State[4] = TS_Yellow
                                        w.ui.pbMSS_1.setPalette(palRed)
                                        w.ui.pbMSN_1.setPalette(palYellow)
                                        TS_State[8] = TS_Yellow
                                        TS_State[12] = TS_Red
                                        w.ui.pbLSS_1.setPalette(palYellow)
                                        w.ui.pbLSN_1.setPalette(palRed)
                            elif lTurnAround:
                                Set_Switches("L", "M")
                                if Local_Dir == "N":
                                    TS_State[10] = TS_Red
                                    Set_Switches("L", "S")
                                else:
                                    TS_State[14] = TS_Red
                                    Set_Switches("L", "N")
                                TS_State[18] = TS_Yellow
                        elif i == 9:                 
                            if TD_State[i]:
                                yLeft2 = True
                                w.ui.pbWyeLD_2.setPalette(palBlue)
                                # lower Boom and start flasher
                                Servo_Control(6,"D")
                                TS_State[20] = TS_Yellow
                                if yLeft1 == False:
                                    TS_State[17] = TS_Yellow
                                    w.ui.pbWyeLSI.setPalette(palYellow)
                                else:
                                    TS_State[17] = TS_Red
                                    w.ui.pbWyeLSI.setPalette(palRed)
                            else:
                                yLeft2 = False
                                w.ui.pbWyeLD_2.setPalette(palBlank)
                                # raise Boom and stop flasher
                                Servo_Control(6,"U")
                                TS_State[20] = TS_Off
                                if yLeft1 == False:
                                    TS_State[17] = TS_Green
                                    w.ui.pbWyeLSI.setPalette(palGreen)
                                else:
                                    TS_State[17] = TS_Red
                                    w.ui.pbWyeLSI.setPalette(palRed)
                        elif i == 10:
                            if TD_State[i]:
                                yRight = True
                                w.ui.pbWyeRD.setPalette(palBlue)
                                TS_State[16] = TS_Red
                                w.ui.pbWyeRSI.setPalette(palRed)
                            else:
                                w.ui.pbWyeRD.setPalette(palBlank)
                                TS_State[16] = TS_Green
                                w.ui.pbWyeRSI.setPalette(palGreen)
                        else:
                                return
                elif TD_Type[i] == "S":
                    # if lp1:
                    if TD_State[11]:
                        # At the Station detected
                        if lohi:
                            if lAtSta:
                                if ctLps:
                                    ctLps = False
                                    w.ui.lblLocal_Arriv.setText("Departing")
                                    Set_Signals("L",Local_Dir,"Y")
                            elif mAtSta:
                                if ctLps:
                                    ctLps = False
                                    w.ui.lblMain_Arriv.setText("Departing")
                            if ((MoverL and mToSta) or lToSta):
                                if lToSta:
                                    lToSta = False
                                    lAtSta = True
                                    w.ui.lblLocal_Arriv.setText("Arrived")
                                    w.ui.pbLStation.setPalette(palAtSta)
                                    if lTurnAround and lTurned:
                                        lTurnAround = False
                                        lTurned = False
                                        lTripMiles = 0.0
                                        if Local_Dir == "S":
                                            lPtr+=1
                                            LocalMiles = lTtl_Dn[lPtr]
                                            lToStnMiles = Loc_M_NS[lPtr]
                                            lMilesToNext = float(Loc_M_NS[lPtr])
                                        else:
                                            lPtr-=1
                                            LocalMiles = lTtl_Up[lPtr]
                                            lToStnMiles = Loc_M_NS[lPtr]
                                            lMilesToNext = float(Loc_M_NS[lPtr-1])
                                        # displayLocalMiles()
                                    # else:
                                    # start at station timer
                                    lpCtr = int(0)
                                    if lPtr == 7:       # New Haven
                                        staDelay = fiveMin
                                    else:
                                        staDelay = oneMin/5     # to speed up for testing
                                    ctLps = True
                                    if Local_Dir == "S":
                                        w.ui.lblLocStaNm.setText(CleanCt(Local_NS[lPtr], "y"))
                                        w.ui.lblLocal_Arriv.setText("Arrived")      #  CleanCt(Local_NS[lPtr-1],""))
                                        if lPtr < (len(Local_NS)-2):
                                            w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr+1],""))
                                            lMilesToNext = float(Loc_M_NS[lPtr])
                                        else:
                                            w.ui.lblLocal_Dest.setText("")
                                            # start turn-around process
                                            lTurnAround = True
                                            Turn_Around(Local_Dir)
                                        lToStnMiles = Loc_M_NS[lPtr]
                                    else:
                                        # Local_Dir == N
                                        w.ui.lblLocStaNm.setText(CleanCt(Local_NS[lPtr],"y"))
                                        w.ui.lblLocal_Arriv.setText("Arrived")
                                        if lPtr>1 and lPtr < (len(Local_NS)-1):
                                            if lPtr < (len(Local_NS)-2):
                                                w.ui.lblLocal_Arriv.setText(CleanCt(Local_NS[lPtr+1],""))
                                            w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr-1],""))
                                            lMilesToNext = float(Loc_M_NS[lPtr-1])
                                        else:
                                            # start turn-around process
                                            lTurnAround = True
                                            Turn_Around(Local_Dir)
                                        lToStnMiles = Loc_M_NS[lPtr-1]
                                    displayLocalMiles()
                                elif mToSta and lsiding:
                                    mToSta = False
                                    mAtSta = True
                                    w.ui.lblMain_Arriv.setText("Arrived")
                                    w.ui.pbLStation.setPalette(palAtSta)
                                    if mTurnAround and mTurned:
                                        mTurnAround = False
                                        mTurned = False
                                        mTripMiles = 0.0
                                        if Main_Dir == "S":
                                            # mPtr+=1
                                            MainMiles = mTtl_Dn[mPtr]
                                            mToStnMiles = Main_M_NS[mPtr]
                                            mMilesToNext = float(Main_M_NS[mPtr])
                                        else:
                                            # mPtr-=1
                                            MainMiles = mTtl_Up[mPtr]
                                            mToStnMiles = Main_M_SN[mPtr]
                                            mMilesToNext = float(Main_M_NS[mPtr-1])
                                        # displayMainMiles()
                                    # else:
                                    # start at station timer
                                    lpCtr = int(0)
                                    if mPtr == 6:       # New York
                                        staDelay = fiveMin
                                    else:
                                        staDelay = oneMin/5     # to speed up for testing
                                    ctLps = True
                                    if Main_Dir == "S":
                                        # mPtr+=1
                                        w.ui.lblMainStaNm.setText(Main_NS[mPtr])
                                        w.ui.lblMain_Arriv.setText("Arrived")
                                        if mPtr < (len(Main_NS)-2):
                                            w.ui.lblMain_Dest.setText(Main_NS[mPtr+1])
                                            mMilesToNext = float(Main_M_NS[mPtr])
                                        else:
                                            w.ui.lblMain_Dest.setText("")
                                            # start turn-around process
                                            mTurnAround = True
                                            Turn_Around(Main_Dir)
                                        mToStnMiles = Main_M_NS[mPtr]
                                    else:
                                        # Main_Dir == N
                                        # mPtr-=1
                                        w.ui.lblMainStaNm.setText(Main_NS[mPtr])
                                        w.ui.lblMain_Arriv.setText("Arrived")
                                        if mPtr>1 and mPtr < (len(Main_NS)-1):
                                            if mPtr < (len(Main_NS)-2):
                                                w.ui.lblMain_Arriv.setText(Main_NS[mPtr+1])
                                            w.ui.lblMain_Dest.setText(Main_NS[mPtr-1])
                                            mMilesToNext = float(Main_M_NS[mPtr-1])
                                        else:
                                            # start turn-around process
                                            mTurnAround = True
                                            Turn_Around(Main_Dir)
                                        mToStnMiles = Main_M_NS[mPtr-1]
                                    displayMainMiles()
                    else:
                        if hilo:
                            if (mAtSta or lAtSta):
                                # leaving station
                                if mAtSta:
                                    mAtSta = False
                                    mLvgSta = True
                                    w.ui.pbLStation.setPalette(palAwaySta)
                                    w.ui.lblMain_Arriv.setText("Departed")
                                    if Main_Dir == "S":
                                        mPtr += 1
                                        w.ui.lblMainStaNm.setText(Main_NS[mPtr])
                                        if mPtr < (len(Main_M_NS)-1):
                                            w.ui.lblMain_Arriv.setText(Main_NS[mPtr-1])
                                            if mPtr<(len(Main_NS)-2):
                                                w.ui.lblMain_Dest.setText(Main_NS[mPtr+1])
                                                mMilesToNext = float(Main_M_NS[mPtr])
                                            else:
                                                w.ui.lblMain_Dest.setText("")
                                            mToStnMiles = Main_M_NS[mPtr-1]
                                            displayMainMiles()
                                        # else:
                                        #     # start Main Turn-around process
                                        #     mTurnAround = True
                                        #     Turn_Around(Main_Dir)
                                    else:
                                        # main Direction == N
                                        mPtr -= 1
                                        w.ui.lblMainStaNm.setText(Main_NS[mPtr])
                                        if mPtr>=1:
                                            w.ui.lblMain_Arriv.setText(Main_NS[mPtr+1])
                                            if mPtr<(len(Main_NS)-1) :
                                                w.ui.lblMain_Dest.setText(Main_NS[mPtr-1])
                                                mMilesToNext = float(Main_M_NS[mPtr])
                                            else:
                                                w.ui.lblMain_Arriv.setText("")
                                            mToStnMiles = Main_M_NS[mPtr]
                                        else:
                                            # in North Yard
                                            mMilesToNext = 0.0
                                            mToStnMiles = 0.0
                                        displayMainMiles()
                                    # if mPtr == 0 or mPtr == len(Main_NS):
                                    #     # time to turn around and go in opppsite direction
                                    #     if Main_Dir == "S":
                                    #         Main_Dir = "N"
                                    #     else:
                                    #         Main_Dir = "S"
                                    # if Main_Dir == "S":
                                    #     mPtr += 1
                                    #     w.ui.lblMainStaNm.setText(Main_NS[mPtr])
                                    # else:
                                    #     mPtr -= 1
                                    #     w.ui.lblMainStaNm.setText(Main_NS[mPtr])
                                    # mToStnMiles = Main_M_NS[mPtr]
                                    # displayMainMiles()
                                elif lAtSta:
                                    lAtSta = False
                                    w.ui.pbLStation.setPalette(palAwaySta)
                                    w.ui.lblLocal_Arriv.setText("Departed")
                                    lToStnMiles = 0.0
                                    if Local_Dir == "S":
                                        lPtr += 1
                                        w.ui.lblLocStaNm.setText(CleanCt(Local_NS[lPtr], "y"))
                                        if lPtr < (len(Local_NS) - 1):
                                            w.ui.lblLocal_Arriv.setText(CleanCt(Local_NS[lPtr-1],""))
                                            if lPtr < (len(Local_NS)-2):
                                                w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr+1],""))
                                                lMilesToNext = float(Loc_M_NS[lPtr])
                                            else:
                                                w.ui.lblLocal_Dest.setText("")
                                            lToStnMiles = Loc_M_NS[lPtr-1]      # was lPtr
                                            displayLocalMiles()
                                        # else:
                                        #     # start turn-around process
                                        #     lTurnAround = True
                                        #     Turn_Around(Local_Dir)
                                    else:   
                                        # Local_Dir == N
                                        lPtr -= 1
                                        w.ui.lblLocStaNm.setText(CleanCt(Local_NS[lPtr],"y"))
                                        if lPtr>=1:
                                            w.ui.lblLocal_Arriv.setText(CleanCt(Local_NS[lPtr+1],""))
                                            if lPtr<(len(Local_NS)-1) :
                                                w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr-1],""))
                                                lMilesToNext = float(Loc_M_NS[lPtr])
                                            else:
                                                w.ui.lblLocal_Arriv.setText("")
                                            lToStnMiles = Loc_M_NS[lPtr]      # was lPtr
                                        else:
                                            # in North Yard
                                            lMilesToNext = 0.0
                                            lToStnMiles = 0.0
                                        displayLocalMiles()
                                        # else:
                                        #     # start turn-around process
                                        #     lTurnAround = True
                                        #     Turn_Around(Local_Dir)
                            TS_State[21]=TS_Off
            else:
                if det == 0 and TD_DBnc[i] != 0:
                    TD_DBnc[i] -= 1

                # scope timing tests
                # if lp1 == False:
                #     if i == 8:
                #         TS_State[17] = TS_Green
                #         w.ui.pbWyeLSI.setPalette(palGreen)
                #     elif i == 9:
                #         TS_State[17] = TS_Green
                #         w.ui.pbWyeLSI.setPalette(palGreen)
                #     elif i == 10:
                #         TS_State[16] = TS_Green
                #         w.ui.pbWyeRSI.setPalette(palGreen)

    lp1 = True
    if ctLps:
        lpCtr += 1
        if lpCtr == staDelay:
            TD_State[11] = 0
            TD_DBnc[11] = 0

def displayLocalMiles():
    global LocalMiles, lMilesToNext, lTripMiles, lMilesToNext

    w.ui.lTotalMiles.setText(str(int(LocalMiles)))
    # w.ui.lMilesToNext.setText(str("%.2f" % lMilesToNext))

    w.ui.lMilesTraveled.setText(str("%.2f" % lTripMiles))
    w.ui.lMilesToSta.setText(str("%.2f" % lToStnMiles))

def displayMainMiles():
    global MainMiles, mMilesToNext, mTripMiles, mMilesToNext

    w.ui.mTotalMiles.setText(str(int(MainMiles)))
    # w.ui.mMilesToNext.setText(str("%.2f" % mMilesToNext))

    w.ui.mMilesTraveled.setText(str("%.2f" % mTripMiles))
    w.ui.mMilesToSta.setText(str("%.2f" % mToStnMiles))
                

def Servo_Control(sv, pos):
    global SV_Type
    
    typ = SV_Type[sv]
    if (typ == TO_Right):
        if (pos == SW_Main):                    # main line
            kit.servo[sv].angle = SW_MinDeg
            sleep(0.1)
            kit.servo[sv].angle = (SW_MinDeg + 5)
        else:                                   # turnout
            kit.servo[sv].angle =  SW_MaxDeg
            sleep(0.1)
            kit.servo[sv].angle = (SW_MaxDeg - 5)
    elif (typ == TO_Left):
        if (pos == SW_Main):                    # main line
            kit.servo[sv].angle = SW_MaxDeg
            sleep(0.1)
            kit.servo[sv].angle = (SW_MaxDeg - 5)
        else:                                   # turnout
            kit.servo[sv].angle =  SW_MinDeg
            sleep(0.1)
            kit.servo[sv].angle = (SW_MinDeg + 5)
    elif (typ == TO_Wye):
        if (pos == SW_Main):                    # main line
            kit.servo[sv].angle = (SW_MaxDeg+10)
            sleep(0.2)
            kit.servo[sv].angle = (SW_MaxDeg - 5)
        else:                                   # turnout
            kit.servo[sv].angle =  (SW_MinDeg+10)
            sleep(0.2)
            kit.servo[sv].angle = (SW_MinDeg + 5)
    elif (typ == Boom):
        if (pos == BM_Up):
            kit.servo[sv].angle = BM_Min_Deg
        else:
            kit.servo[sv].angle = BM_Max_Deg
    SV_State[sv] = pos

    return(1)

def ToggleDet(msg):
    trk = msg[0]
    det = int(msg[1])
    if trk == "L":
        # toggle Local Detector
        det = (det*4)-1
        # Servo_Control()
        
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

# read and load track inventory file
def Load_Track_Inventory():
    global SV_Type, TS_Type, TD_Type, TrackInventoryVer, \
           lToStnMiles, lTripMiles, LScale, mToStnMiles, mTripMiles, MScale

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
    except:
        filename = ""
        TrackInventoryVer = 0.0

def Default_Switches():
    Set_Switches("M","M")
    Set_Switches("L","M")

def Save_Train_State(fN):
    global  TrackStateVer, SV_State, TS_State, TD_Type, \
            SV_Type, TS_Type, TD_Type, TrackInventoryVer, \
            MainStation, mToStnMiles, mTripMiles, MScale, \
            mPtr,  mDetMiles, Main_Dir, MT_Pos, \
            LocalStation, lToStnMiles, lTripMiles, LScale, \
            lPtr, lDetMiles, Local_Dir, LT_Pos

    # Change name of current invertory file to *.bak
    try:
        # get version
        f = open("./"+fN+".ses")
        lines = f.readlines()
        line = lines[3]
        TrackStateVer = float(line.strip("\n"))
        
        # back up previous version
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
    f = open(fNew, "wt")
    f.write("Session State\n\n")

    # Update and write version
    f.write("Version:\n")
    f.write("{:5.3f}".format(TrackStateVer + 0.001) + "\n\n")

    # write time stamp
    # t = time()
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

    # Save Last Positions of Trains
    f.write("Last Main Train Position:\n")
    f.write(str(MT_Pos) + "\n")
    f.write("Last Local Train Position:\n")
    f.write(str(LT_Pos) + "\n\n")

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

    # Save Train Positions and Routes
    line = ""
    f.write("Acela Route Selection\n")
    f.write(("Main Station:")+"\n")
    f.write(Main_NS[mPtr]+"\n")
    f.write("Main Ptr:\n")
    f.write(str(mPtr)+"\n")
    f.write("Direction:\n")
    f.write(Main_Dir+"\n")
    f.write("Main Miles:\n")
    f.write(str(MainMiles)+"\n")
    f.write("Miles To Station:\n")
    f.write(str(mToStnMiles)+"\n")
    f.write("Trip Miles:\n")
    f.write(str(mTripMiles)+"\n")
    f.write("Scale:\n")
    f.write(str(MScale)+"\n\n")

    f.write("CT Route Selection\n")
    f.write(("Local Station:")+"\n")
    f.write(Local_NS[lPtr]+"\n")
    f.write("Local Ptr:\n")
    f.write(str(lPtr)+"\n")
    f.write("Direction:\n")
    f.write(Local_Dir+"\n")
    f.write("Local Miles:\n")
    f.write(str(LocalMiles)+"\n")
    f.write("Miles To Station:\n")
    f.write(str(lToStnMiles)+"\n")
    f.write("Trip Miles:\n")
    f.write(str(lTripMiles)+"\n")
    f.write("Scale:\n")
    f.write(str(LScale)+"\n")
    f.close()

def TurnOffHardware():
    # Signals all off
    Set_Signals("A", "A", "O")
    # All switches to main
    Default_Switches()

def LoadCurSession(fn):
    global  TrackStateVer, SV_State, TS_State, TD_Type, \
            SV_Type, TS_Type, TD_Type, TrackInventoryVer, \
            MainStation, mToStnMiles, mTripMiles, MScale, \
            mPtr, mDetMiles, Main_Dir, MainMiles, MT_Pos, \
            LocalStation, lToStnMiles, lTripMiles, LScale, \
            lPtr, lDetMiles, Local_Dir, LocalMiles, LT_Pos

    TrackStateVer = 0.0
    # filename = "Session.ses" 
    try:
        if fn == False:
            fn = "CurSession"
        f = open("./"+fn+".ses")
        lines = f.readlines()
        line = lines[3]
        TrackStateVer = float(line.strip("\n"))

        line = lines[8].strip("\n")
        SV_State = line.split(", ")
        if SV_State[15] == "":
            SV_State[15] = " "

        line = lines[11].strip("\n")
        TD_State = line.split(", ")
        if TD_State[15] == "":
            TD_State[15] = " "

        line = lines[14].strip("\n")
        MT_Pos = line
        line = lines[16].strip("\n")
        LT_Pos = line

        line = lines[19].strip("\n")
        TS_State = line.split(", ")
        if TS_State[23] == "":
            TS_State[23] = " "

        # Acela Data
        line = lines[23].strip("\n")
        MainStation = line
        line = lines[25].strip("\n")
        mPtr = int(line)
        line = lines[27].strip("\n")
        Main_Dir = line
        line = lines[29].strip("\n")
        MainMiles = float(line)
        line = lines[31].strip("\n")
        mToStnMiles = float(line)
        line = lines[33].strip("\n")
        mTripMiles = float(line)
        line = lines[35].strip("\n")
        MScale = int(line)

        # CT Shore Data
        line = lines[39].strip("\n")
        LocalStation = line
        line = lines[41].strip("\n")
        lPtr = int(line)
        line = lines[43].strip("\n")
        Local_Dir = line
        line = lines[45].strip("\n")
        LocalMiles= float(line)
        line = lines[47].strip("\n")
        lToStnMiles = float(line)
        line = lines[49].strip("\n")
        lTripMiles = float(line)
        line = lines[51].strip("\n")
        LScale = int(line)

        Load_Acela_Data(True)

        Load_CT_Data(True)

        f.close()
        TS_Blinker()
    except:
        filename = ""
        TrackStateVer = 0.0

def SaveSession():
    global SessionName
    Save_Train_State(SessionName)

def LoadSession():
    global SessionName, Testing, RunDets
    LoadCurSession(SessionName)
    Testing = False
    RunDets = 3

def ClearDetectors():
    w.ui.pbMD_1.setPalette(palBlank)
    w.ui.pbMD_2.setPalette(palBlank)
    w.ui.pbMD_3.setPalette(palBlank)
    w.ui.pbMD_4.setPalette(palBlank)
    w.ui.pbLD_1.setPalette(palBlank)
    w.ui.pbLD_2.setPalette(palBlank)
    w.ui.pbLD_3.setPalette(palBlank)
    w.ui.pbLD_4.setPalette(palBlank)
    w.ui.pbWyeLD_1.setPalette(palBlank)
    w.ui.pbWyeLD_2.setPalette(palBlank)
    w.ui.pbWyeRD.setPalette(palBlank)

def Set_Switches(Line, Dir):
    global SV_Type
    
    pal = QPalette()
    if Line == "M":
        if Dir == "M":
            pal = palBlack
            w.ui.lineM_Sw1.setPalette(pal)
            Servo_Control(0,"M")      # 0 and 3 wired together
            w.ui.lineL_Sw1.setPalette(pal)
            Servo_Control(1,"M")      # 1 and 4 wired together
            pal = palBlnk
            w.ui.lineM_SwR1.setPalette(pal)
            w.ui.lineM_SwR2.setPalette(pal)
            w.ui.lineM_SwR3.setPalette(pal)
            w.ui.lineM_SwL4.setPalette(pal)
            w.ui.lineM_SwR5.setPalette(pal)
            w.ui.lineM_SwR6.setPalette(pal)
            w.ui.lineM_SwR7.setPalette(pal)
            w.ui.lineM_SwL1.setPalette(pal)
            w.ui.lineM_SwL2.setPalette(pal)
            w.ui.lineM_SwL3.setPalette(pal)
            w.ui.lineM_SwL4.setPalette(pal)
            w.ui.lineM_SwL5.setPalette(pal)
            w.ui.lineM_SwL6.setPalette(pal)
            w.ui.lineM_SwL7.setPalette(pal)
        elif Dir == "S":
            pal = palBlnk
            Servo_Control(0,"S")      # 0 and 3 wired together
            w.ui.lineM_Sw1.setPalette(pal)
            w.ui.lineL_Sw1.setPalette(pal)
            # Servo_Control(3,"S")    # 0 and 3 wired together
            pal = palBlack
            w.ui.lineM_SwR1.setPalette(pal)
            w.ui.lineM_SwR2.setPalette(pal)
            w.ui.lineM_SwR3.setPalette(pal)
            w.ui.lineM_SwL4.setPalette(pal)
            w.ui.lineM_SwR5.setPalette(pal)
            w.ui.lineM_SwR6.setPalette(pal)
            w.ui.lineM_SwR7.setPalette(pal)
        elif Dir == "N":
            pal = palBlnk
            Servo_Control(1,"S")      # 0 and 3 wired together
            w.ui.lineM_Sw1.setPalette(pal)
            w.ui.lineL_Sw1.setPalette(pal)
            pal = palBlack
            w.ui.lineM_SwL1.setPalette(pal)
            w.ui.lineM_SwL2.setPalette(pal)
            w.ui.lineM_SwL3.setPalette(pal)
            w.ui.lineM_SwL4.setPalette(pal)
            w.ui.lineM_SwL5.setPalette(pal)
            w.ui.lineM_SwL6.setPalette(pal)
            w.ui.lineM_SwL7.setPalette(pal)
    elif Line == "L":
        if Dir == "M":
            pal = palBlack
            Servo_Control(2,"M")
            Servo_Control(3,"M")
            w.ui.lineL_Sw2.setPalette(pal)
            # Servo_Control(3,"M")      # 1 and 2 wired together
            pal = palBlnk
            w.ui.lineL_SwR1.setPalette(pal)
            w.ui.lineL_SwR2.setPalette(pal)
            w.ui.lineL_SwR3.setPalette(pal)
            w.ui.lineL_SwL1.setPalette(pal)
            w.ui.lineL_SwL2.setPalette(pal)
            w.ui.lineL_SwL3.setPalette(pal)
        elif Dir == "S":
            pal = palBlnk
            Servo_Control(2,"S")
            Servo_Control(4,"M")    # move Wye1 to match
            w.ui.lineL_Sw2.setPalette(pal)
            pal = palBlack
            w.ui.lineL_SwR1.setPalette(pal)
            w.ui.lineL_SwR2.setPalette(pal)
            w.ui.lineL_SwR3.setPalette(pal)
        elif Dir == "N":
            pal = palBlnk
            Servo_Control(3,"S")
            Servo_Control(4,"R")    # move Wye1 to match
            w.ui.lineL_Sw2.setPalette(pal)
            # Servo_Control(3,"S")      # 1 and 2 wired together
            pal = palBlack
            w.ui.lineL_SwL1.setPalette(pal)
            w.ui.lineL_SwL2.setPalette(pal)
            w.ui.lineL_SwL3.setPalette(pal)
    elif Line == "W":
        if Dir == "L":
            Servo_Control(4,"M")
            # pal = palBlack
            # w.ui.lineL_Sw2.setPalette(pal)
            # pal = palBlnk
            # w.ui.lineL_SwL1.setPalette(pal)
            # w.ui.lineL_SwL2.setPalette(pal)
            # w.ui.lineL_SwL3.setPalette(pal)
        elif Dir == "R":
            Servo_Control(4,"S")
            # pal = palBlnk
            # w.ui.lineL_Sw2.setPalette(pal)
            # w.ui.lineL_SwL1.setPalette(pal)
            # w.ui.lineL_SwL2.setPalette(pal)
            # w.ui.lineL_SwL3.setPalette(pal)
            # pal = palBlack
            # w.ui.lineL_SwR1.setPalette(pal)
            # w.ui.lineL_SwR2.setPalette(pal)
            # w.ui.lineL_SwR3.setPalette(pal)
    elif Line == "Y":
        if Dir == "L":
            pal = palBlnk
            w.ui.lineWye2R_1.setPalette(pal)
            w.ui.lineWye2R_2.setPalette(pal)
            w.ui.lineWye2R_3.setPalette(pal)
            Servo_Control(5,"M")
            pal = palBlack
            w.ui.lineWye2L_1.setPalette(pal)
            w.ui.lineWye2L_2.setPalette(pal)
            w.ui.lineWye2L_3.setPalette(pal)
        elif Dir == "R":
            pal = palBlnk
            w.ui.lineWye2L_1.setPalette(pal)
            w.ui.lineWye2L_2.setPalette(pal)
            w.ui.lineWye2L_3.setPalette(pal)
            Servo_Control(5,"S")
            pal = palBlack
            w.ui.lineWye2R_1.setPalette(pal)
            w.ui.lineWye2R_2.setPalette(pal)
            w.ui.lineWye2R_3.setPalette(pal)

def Test_Boom(UD):
    Servo_Control(6, UD)
    St = TS_Off
    if UD == "D":
        St = TS_Yellow
    TS_State[20] = St

def Set_Signals(Trk, Dir, St):
    global TS_State, TS_Type

    pal = QPalette()
    if St == "G":
        pal = palGreen
    elif St == "R":
        pal = palRed
    elif St == TS_Yellow:
        pal = palYellow
    elif St == "F":
        pal = palRed
    elif St == "O":
        pal = palBlank
    else:
        pal = palBlank

    if Trk == "M":
        if Dir == "S":
            # Test Main N to S
            TS_State[0] = St
            TS_State[1] = St
            TS_State[2] = St
            TS_State[3] = St
            w.ui.pbMSS_1.setPalette(pal)
            w.ui.pbMSS_2.setPalette(pal)
            w.ui.pbMSS_3.setPalette(pal)
            w.ui.pbMSS_4.setPalette(pal)
        else:
            # Test Main S to N
            TS_State[4] = St
            TS_State[5] = St
            TS_State[6] = St
            TS_State[7] = St
            w.ui.pbMSN_1.setPalette(pal)
            w.ui.pbMSN_2.setPalette(pal)
            w.ui.pbMSN_3.setPalette(pal)
            w.ui.pbMSN_4.setPalette(pal)
    elif Trk == "L":
        if Dir == "S":
            # Test Local N to S
            TS_State[8] = St
            TS_State[9] = St
            TS_State[10] = St
            TS_State[11] = St
            w.ui.pbLSS_1.setPalette(pal)
            w.ui.pbLSS_2.setPalette(pal)
            w.ui.pbLSS_3.setPalette(pal)
            w.ui.pbLSS_4.setPalette(pal)
        else:
            # Test Local S to N
            TS_State[12] = St
            TS_State[13] = St
            TS_State[14] = St
            TS_State[15] = St
            w.ui.pbLSN_1.setPalette(pal)
            w.ui.pbLSN_2.setPalette(pal)
            w.ui.pbLSN_3.setPalette(pal)
            w.ui.pbLSN_4.setPalette(pal)
    elif Trk == "W":
        # Wye Signals
        if Dir == "I":
            TS_State[16] = St
            TS_State[17] = St
            w.ui.pbWyeRSI.setPalette(pal)
            w.ui.pbWyeLSI.setPalette(pal)
        else:
            TS_State[18] = St
            TS_State[19] = St
            w.ui.pbWyeLSO.setPalette(pal)
            w.ui.pbWyeRSO.setPalette(pal)
    elif Trk == "B":
        TS_State[20] = St   # Boom
    elif Trk == "F":
        TS_State[21] = St
        TS_State[22] = St
        TS_State[23] = St
    elif Trk == "A":
        if Dir == "A":
            if St == "O":
                # turn all signals off
                for i in range(len(TS_Type)):
                    TS_State[i] = St
                w.ui.pbMSS_1.setPalette(pal)
                w.ui.pbMSS_2.setPalette(pal)
                w.ui.pbMSS_3.setPalette(pal)
                w.ui.pbMSS_4.setPalette(pal)
                w.ui.pbMSN_1.setPalette(pal)
                w.ui.pbMSN_2.setPalette(pal)
                w.ui.pbMSN_3.setPalette(pal)
                w.ui.pbMSN_4.setPalette(pal)
                w.ui.pbLSS_1.setPalette(pal)
                w.ui.pbLSS_2.setPalette(pal)
                w.ui.pbLSS_3.setPalette(pal)
                w.ui.pbLSS_4.setPalette(pal)
                w.ui.pbLSN_1.setPalette(pal)
                w.ui.pbLSN_2.setPalette(pal)
                w.ui.pbLSN_3.setPalette(pal)
                w.ui.pbLSN_4.setPalette(pal)
                w.ui.pbWyeRSI.setPalette(pal)
                w.ui.pbWyeLSI.setPalette(pal)
                w.ui.pbWyeLSO.setPalette(pal)
                w.ui.pbWyeRSO.setPalette(pal)

def CleanCt(namStr, stnam):
    newStr = ""
    if namStr.find("(S)")>0:
        newStr = namStr.replace("(S)","")
        if stnam=="y":
            w.ui.lblLocalLine.setText(NLine)
    else:
        newStr=namStr.replace("(M)","")
        if stnam=="y":
            w.ui.lblLocalLine.setText(SLine)
    return(newStr)

def Load_CT_Data(fFile):
    global  lToStnMiles, lTripMiles, LScale, lPtr, lDetMiles, \
            Local_Dir, LocalMiles, lMilesToNext, Testing, \
            lToSta, lTtl_Dn, lTtl_Up

    # Load CT Shore Start point and direction of travel
    if (fFile == False):
        LocalMiles = 0.0
    Set_Signals("W","O","R")
    w.ui.lblLocStaNm.setText(CleanCt(Local_NS[lPtr], "y"))
    lTripMiles = 0.0
    lDetMiles = float(LScale / 4)
    if Local_Dir == "S":
        # Set North bound signals to red
        Set_Signals("L","N","R")
        w.ui.lblL_L.setText("L")
        w.ui.lblL_R.setText("SB")
        lMilesToNext = float(Loc_M_NS[lPtr])    #17
        if (lPtr>0 and lPtr!=len(Local_NS)-1):
            # At Station
            w.ui.lblLocal_Arriv.setText("Arriving")      #CleanCt(Local_NS[lPtr-1],""))
            if lPtr < (len(Local_NS)-1):
                w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr+1],""))
            else:
                w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr],""))
        else:
            # Comming from yard
            w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr+1],"y"))
            w.ui.lblLocal_Arriv.setText("")
            lToSta = True
        LocalMiles = lTtl_Dn[lPtr]
        # lToStnMiles = Loc_M_NS[lPtr]
    else:
        # Set South bound signals to red
        Set_Signals("L","S","R")
        w.ui.lblL_L.setText("NB")
        w.ui.lblL_R.setText("L")
        lMilesToNext = float(Loc_M_NS[lPtr-1])      #1
        lTripMiles = 0.0
        if lPtr<(len(Local_NS)-1) and lPtr>0:
            w.ui.lblLocal_Arriv.setText("Arriving")      # CleanCt(Local_NS[lPtr+1],""))
            if lPtr>0:
                w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr-1],"y"))
            else:
                w.ui.lblLocal_Arriv.setText(CleanCt(Local_NS[lPtr]))
        else:
            w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr-1],"y"))
            w.ui.lblLocal_Arriv.setText("")
            lToSta = True
        LocalMiles = lTtl_Up[lPtr]
        # lToStnMiles = Loc_M_NS[lPtr-1]
    displayLocalMiles()
    # lLeavingSta = True

def Load_Acela_Data(fFile):
    global  mToStnMiles, mTripMiles, MScale, mPtr, mAtSta, mToSta, \
            Main_Dir, MainMiles, mMilesToNext,  mDetMiles, \
            mLvgSta, Testing, MoverL, mTtl_Dn, mTtl_Up

    # Load Acela Start point and direction of travel
    if (fFile == False):
        MainMiles = 0.0
    w.ui.lblMainStaNm.setText(Main_NS[mPtr])
    mTripMiles = 0.0
    # MoverL = True
    # mToSta = True
    mDetMiles = float(MScale / 4)
    if Main_Dir == "S":
        # Set North bound signals to red
        Set_Signals("M","N","R")
        w.ui.lblM_L.setText("M")
        w.ui.lblM_R.setText("SB") 
        mMilesToNext = Main_M_NS[mPtr]
        if mPtr>0 and mPtr!=len(Main_NS)-1:
            w.ui.lblMain_Arriv.setText("Arriving")
            if mPtr < (len(Main_NS)-1):
                w.ui.lblMain_Dest.setText(Main_NS[mPtr+1])
            else:
                w.ui.lblMain_Dest.setText(Main_NS[mPtr])
        else:
            w.ui.lblMain_Dest.setText(Main_NS[mPtr+1])
            w.ui.lblMain_Arriv.setText("")
        MainMiles = mTtl_Dn[mPtr]
        # mToStnMiles = Main_M_NS[mPtr]
    else:
        # Set South bound signals to red
        Set_Signals("M","S","R")
        w.ui.lblM_L.setText("NB")
        w.ui.lblM_R.setText("M")
        mMilesToNext = Main_M_NS[mPtr-1]
        mTripMiles = 0.0
        if mPtr<(len(Main_NS)-2):
            w.ui.lblMain_Arriv.setText("Arriving")
            if mPtr<(len(Main_NS)-1) :
                w.ui.lblMain_Dest.setText(Main_NS[mPtr-1])
            else:
                w.ui.lblMain_Arriv.setText(Main_NS[mPtr+1])
        else:
            w.ui.lblMain_Dest.setText(Main_NS[mPtr-1])
            w.ui.lblMain_Arriv.setText("")
        MainMiles = mTtl_Up[mPtr]
        # mToStnMiles = Main_M_SN[mPtr-1]
    displayMainMiles()
    # mLeavingSta = True

def startAcela():
    global Testing, RunDets, Main_Dir, MoverL, mToSta

    if Main_Dir=="S":
        dir = "N"
    else:
        dir = "S"
    Set_Signals("M", dir, "R")
    Default_Switches()
    # if TrnDet.read_pin(11):
    #     mAtSta = True
    MoverL = True
    # mToSta = True
    Testing = False
    RunDets = 1

def startCTShore():
    global Testing, RunDets, Local_Dir, lToSta, lAtSta

    if Local_Dir=="S":
        dir = "N"
    else:
        dir = "S"
    Set_Signals("L", dir, "R")
    Default_Switches()
    if TrnDet.read_pin(11):
        lAtSta = True
        w.ui.lblLocal_Arriv.setText("Arrived")    
    TS_State[21]=TS_On
    lToSta = True
    Testing = False
    RunDets = 2

def startBoth():
    global Testing, RunDets

    startAcela()
    startCTShore()
    RunDets = 3

def ShowMsg():
    global timeMDir, timeMD, timeMPre, timeM, timeLDir, timeLD, timeLPre, timeL
    # global MT_Pos, LT_Pos, mPtr, lPtr, Time2, timeDir
    # w.ui.statusBar.showMessage("MPos = " + str(MT_Pos)+"  LPos = " + str(LT_Pos) + "  mPtr = " + str(mPtr) + "  lPtr = " + str(lPtr) + "  Train Time = " + str(Time2), 0)
    w.ui.statusBar.showMessage("Main Dir = " + timeMDir + "  Main Speed = " + str("%.1f" % mainSpd), 0)


class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_mwinAI_Train()
        self.ui.setupUi(self)

        Load_Track_Inventory()

        # clear Direction Indicators
        self.ui.lblM_L.setText("")
        self.ui.lblM_R.setText("")
        self.ui.lblL_L.setText("")
        self.ui.lblL_R.setText("")

        fnt = QFont()
        fnt.setPointSize(12)
        self.ui.statusBar.setFont(fnt)

        # set Station Color
        self.ui.pbLStation.setPalette(palAwaySta)
        # Turn Off Station Light
        TS_State[21] = TS_Off

        def CT_Shore():
            global lPtr, Local_Dir, LScale, Local_NS, lExpress
            
            dlgwin = QDialog()
            dlgC = Ui_dlgCTStPt()
            dlgC.setupUi(dlgwin)
            dlgC.cbxCtShorStartPt.addItems(Local_NS)
            if dlgwin.exec_():
                lPtr = dlgC.cbxCtShorStartPt.currentIndex()
                Local_Dir = dlgC.cbxCtShoreDir.currentText()[0]
                LScale = dlgC.sbxScale.value()
                lExpress = dlgC.cbxExpress.isChecked()
                Load_CT_Data(False)

        def AcelaStPt():
            global mPtr, Main_Dir, MScale, Main_NS, mExpress

            dlgwin = QDialog()
            dlgA = Ui_dlgAcelaStPt()
            dlgA.setupUi(dlgwin)
            dlgA.cbxAcelaStartPt.addItems(Main_NS)
            if dlgwin.exec_():
                mPtr = dlgA.cbxAcelaStartPt.currentIndex()
                Main_Dir = dlgA.cbxAcelaDir.currentText()[0]
                MScale = dlgA.sbxScale.value()
                mExpress = dlgA.cbxExpress.isChecked()
                Load_Acela_Data(False)

        def FileOpen(SorO):
            global SessionName
            FList = []
            dlgwin = QDialog()
            dlg = Ui_dlgFileOpen()
            dlg.setupUi(dlgwin)
            FList = GenFileList(".ses")
            dlg.cbxFileList.addItems(FList)
            if SorO == "S":
                dlg.cbxFileList.setEditable(True)
            if dlgwin.exec_():
                SessionName = dlg.cbxFileList.currentText().strip(".ses")
                if SorO == "O":
                    LoadSession()
                else:
                    SaveSession()

        def SaveSessionAs():
            FileOpen("S")

        def LoadSessionAs():
            FileOpen("O")

        def Start_Acela():
            startAcela()

        def Start_CTShore():
            startCTShore()

        def Start_Both():
            startBoth()

        def CloseTrainAI():
            global SessionName
            Save_Train_State(SessionName)
            TurnOffHardware()
            self.close()

        # def Toggle(msg):
        #     ToggleDet(msg)

        self.ui.actionAcela.triggered.connect(AcelaStPt)
        self.ui.actionCT_Shore.triggered.connect(CT_Shore)
        self.ui.actionStart_Acela.triggered.connect(Start_Acela)
        self.ui.actionStart_CT_Shore.triggered.connect(Start_CTShore)
        self.ui.actionStart_Both.triggered.connect(Start_Both)
        # # self.ui.actionPreferences.triggered.connect(self.Preferences())
        self.ui.actionQuit.triggered.connect(CloseTrainAI)
        self.ui.actionSavCurSession.triggered.connect(SaveSession)
        self.ui.actionSave_Session_as.triggered.connect(SaveSessionAs)
        self.ui.actionLoad_Last_Session.triggered.connect(LoadSession)
        self.ui.actionLoad_Session.triggered.connect(LoadSessionAs)
        # self.ui.actionLD_1.triggered.connect(Toggle("L1"))
        # self.ui.actionLD_2.triggered.connect(Toggle("L2"))
        # self.ui.actionLD_3.triggered.connect(Toggle("L3"))
        # self.ui.actionLD_4.triggered.connect(Toggle("L4"))
        # # self.ui.actionWL_1.triggered.connect(Toggle("W1"))
        # # self.ui.actionWL_2.triggered.connect(Toggle("W2"))
        # # self.ui.actionWR_1.triggered.connect(Toggle("W3"))
        # self.ui.actionMD_1.triggered.connect(Toggle("M1"))
        # self.ui.actionMD_2.triggered.connect(Toggle("M2"))
        # self.ui.actionMD_3.triggered.connect(Toggle("M3"))
        # self.ui.actionMD_4.triggered.connect(Toggle("M4"))

        self.TTimer = QTimer()
        self.TTimer.timeout.connect(TS_Blinker)
        self.TTimer.start(50)

        self.DTimer = QTimer()
        self.DTimer.timeout.connect(ReadDetectors)
        self.DTimer.start(100)

        # self.runTimer = QTimer()
        # self.runTimer.timeout.connect(ShowPos)
        # self.runTimer.start(1000)

app = QApplication(sys.argv)
w = AppWindow()

RunDets = 0
Set_Signals("M","N","R")
Set_Signals("M","S","R")
Set_Signals("L","N","R")
Set_Signals("L","S","R")
Set_Signals("W","I","R")
Set_Signals("W","O","R")
ClearDetectors()

w.show()
#w.move(1984,0)
sys.exit(app.exec_())
   