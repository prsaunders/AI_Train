import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPalette, QTextBlock, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QFormLayout, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QListView, QListWidget, QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent, QFileSelector, QTimer, QTimerEvent, Qt

from IOPi import IOPi
import RPi.GPIO as GPIO
import threading
from time import sleep, time, ctime
from adafruit_servokit import ServoKit

#from Train_Hardware_Test_and_Setup import Save_Train_Inventory

kit = ServoKit(channels=16)
from adafruit_servokit import PCA9685

from datetime import datetime

from AI_Win import Ui_mwinAI_Train
from Acela_Strt_Pt import Ui_dlgAcelaStPt
from CT_Shore_Strt_Pt import Ui_dlgCTStPt
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
#global TrnSig
TrnSig = IOPi(0x21)
TrnSig.set_bus_direction(0X0)
TrnSig.invert_bus(0xFFFF)

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
TD_State = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
TD_Chan = 0

# Train SIgnal Settings
TS_Green = "G"
TS_Yellow = "Y"     # toggles Green/Red
TS_Red = "R"
TS_Off = "O"        # off
TS_On = "B"         # Building/Facility
TS_FlashR = "F"     # causes flashing reds Boom Lights    

#global TS_Type
TS_Type = ["S", "S", "S", "S", "S", "S", "S", "S"]
#global TS_State
TS_State = ["G", "G", "G", "G", "G", "G", "G", "G"]
TS_Ind = [0, 0 , 0, 0, 0 , 0 , 0, 0]
#global TS_Time
TS_Time = [0,0,0,0,0,0,0,0]

TS_Chan = 0

# Train Layout Data Max values
ServoCT = 16        # Channels 1 to 16  (16 max)
TrainDET = 8        # Detectors 1 to 16 (16 max)
TrainSIG = 8        # Signals 1 to 8    (8 max) More reqires another IO_Pi Bd + Plus Interface Bd

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
Main_M_NS = [0, 10, 33, 101, 41, 35, 10, 81, 28, 67, 9, 31, 0]
Main_M_SN = [0, 31, 9, 67, 28, 81, 10, 35, 41, 101, 33, 10, 0]
Main_Dir = 'S'      # S = Moving South, N = Moving North
MScale = 10.0          # miles/loop
MainStation = ""
MainMiles = int(0)
MainLpCt = int(0)
mTripMiles = 0.0
mToStnMiles = 0.0
mMilesToNext = 0.0
mToStnCt = int(0)
mPtr = int(0)
mLeavingSta = False
mToNextCt = 0

Local_NS = ['North Yard(S)',
            'New London(S)', 'Old Saybrook(S)', 'Westbrook(S)', 'Guilford(S)',
            'Branford(S)', 'State Street(S)', 'New Haven(S)', 'West Haven(M)',
            'Milford(M)', 'Stratford(M)', 'Bridgeport(M)', 'Fairfield Metro(M)',
            'Fairfield(M)', 'Westport(M)', 'South Norwalk(M)', 'Stamford(M)',
            'South Yard(M)']
Loc_M_NS = [0, 18, 5, 14, 9, 11, 3, 7, 5, 4, 4, 2, 7, 3, 4, 5, 0]
Loc_M_SN = [0, 5, 4, 3, 7, 2, 4, 4, 5, 7, 3, 11, 9, 14, 5, 18, 0]
NLine = "Shore Line East"
SLine = "Metro North"
Local_Dir = 'S'     # S = Moving South, N = Moving North
LScale = 10          # miles/loop
LocalStation = ""
LocalMiles = int(0)
lTripMiles = 0.0
LocalLpCt = int(0)
lToStnMiles = 0.0     # Derived from LScale of Miles per Loop
lMilesToNext = 0.0
lToStnCt = int(0)
lPtr = int(0)
lLeavingSta = False
lToNextCt = 0

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

def TS_Blinker():
    global TS_Type, TS_State, TrnSig, TS_Time, TS_Ind
    
    for i in range(8):
        if TS_State[i] == TS_Yellow or TS_State[i] == TS_FlashR:
            t = int(TS_Time[i])
            if t == 0:
                if TS_Ind[i] == "0":
                    TS_Ind[i] = "1"
                else:
                    TS_Ind[i] = "0"
                TS_Time[i] = 10
            else:
                t -= 1
                TS_Time[i] = t
        pin = ((i*2)+1)
        state = TS_Ind[i]
        if TS_State[i] == TS_Green:
            TrnSig.write_pin(pin, 0)    # green on
            TrnSig.write_pin(pin+1,1)   # red off
        elif TS_State[i] == TS_Red:
            TrnSig.write_pin(pin+1, 0)  # red on
            TrnSig.write_pin(pin, 1)    # green off
        elif TS_State[i] == TS_FlashR:
            TrnSig.write_pin(pin, 1)        # green off
            TrnSig.write_pin(pin+1,state)   # flashing red
        elif TS_State[i] == TS_Yellow:
            if state==1:
                # green on
                TrnSig.write_pin(pin, 1)
                TrnSig.write_pin((pin+1), 0)
            else:
                TrnSig.write_pin(pin, 0)
                TrnSig.write_pin((pin+1), 1)
        elif TS_State[i] == TS_Off:
            TrnSig.write_pin(pin, 1)
            TrnSig.write_pin(pin+1,1)

def ReadDetectors():
    global  TD_Type, TD_State, MainLpCt, mToStnCt, LocalLpCt, lToStnCt, \
            MainMiles, LocalMiles, mToStnMiles, lToStnMiles, mTripMiles, \
            lTripMiles, mMilesToNext, lMilesToNext, mLeavingSta, mToNextCt, \
            lLeavingSta, lToNextCt   
    det = 0
    l = len(TD_Type)
    for i in range(l-1):
        lohi = False
        det = TrnDet.read_pin(i+1)
        if det != TD_State[i]:
            if TD_State[i] == 0:
                lohi = True
            TD_State[i] = det
            if TD_Type[i] == "D":
                if i < 4:
                    # Main Loop
                    if i == 0:
                        if TD_State[i]:
                            w.ui.pbMD_1.setPalette(palBlue)
                        else:
                            w.ui.pbMD_1.setPalette(palBlank)
                    elif i == 1:
                        if TD_State[i]:
                            w.ui.pbMD_2.setPalette(palBlue)
                        else:
                            w.ui.pbMD_2.setPalette(palBlank)
                    elif i == 2:
                        if TD_State[i]:
                            w.ui.pbMD_3.setPalette(palBlue)
                        else:
                            w.ui.pbMD_3.setPalette(palBlank)
                    elif i == 3:
                        if TD_State[i]:
                            w.ui.pbMD_4.setPalette(palBlue)
                        else:
                            w.ui.pbMD_4.setPalette(palBlank)
                    if lohi == True:
                        # Main Loop Mileage
                        if mLeavingSta:
                            mToNextCt -= 1
                            mMilesToNext = float(mToNextCt)/(MScale * 4)
                        MainLpCt += 1
                        mToStnCt += 1
                        mToStnMiles = float(mToStnCt)/(MScale * 4)
                        mTripMiles += mToStnMiles
                        item = w.ui.tblMtoSta.item(0,0)
                        item.setText(str("%.2f" % mTripMiles))
                        item = w.ui.tblMtoSta.item(1,0)
                        item.setText(str("%.2f" % mToStnMiles))

                        item = w.ui.tblMTrip.item(0,0)
                        item.setText(str("%.2f" % MainMiles))
                        item = w.ui.tblMtoSta.item(1,0)
                        item.setText(str("%.2f" % mMilesToNext))
                elif i < 8:
                    if i == 4:
                        if TD_State[i]:
                            w.ui.pbLD_1.setPalette(palBlue)
                        else:
                            w.ui.pbLD_1.setPalette(palBlank)
                    elif i == 5:
                        if TD_State[i]:
                            w.ui.pbLD_2.setPalette(palBlue)
                        else:
                            w.ui.pbLD_2.setPalette(palBlank)
                    elif i == 6:                                                           
                        if TD_State[i]:
                            w.ui.pbLD_3.setPalette(palBlue)
                        else:
                            w.ui.pbLD_3.setPalette(palBlank)
                    elif i == 7:
                        if TD_State[i]:
                            w.ui.pbLD_4.setPalette(palBlue)
                            if Local_Dir == "N":
                                LocalLpCt += 1
                        else:
                            w.ui.pbLD_4.setPalette(palBlank)
                            if Local_Dir == "S":
                                LocalLpCt += 1
                    # Main Loop Mileage
                    LocalLpCt += 1
                    lToStnCt += 1
                    lToStnMiles = float(lToStnCt)/(LScale * 4)
                    lTripMiles = lTripMiles + lToStnMiles

                    
                elif i < 12:
                    if i == 8:
                        if TD_State[i]:
                            w.ui.pbWyeLD_1.setPalette(palBlue)
                        else:
                            w.ui.pbWyeLD_1.setPalette(palBlank)
                    elif i == 9:                 
                        if TD_State[i]:
                            w.ui.pbWyeLD_2.setPalette(palBlue)
                        else:
                            w.ui.pbWyeLD_2.setPalette(palBlank)
                    else:
                        return

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

def TS_Control(ts, tsColor):
    global TrnSig, TS_Type
    #pin = ((ts * 2)+1)
    TS_Type[ts] = tsColor
    if tsColor == TS_Green:
        TS_State[ts] = "1"
    elif tsColor == TS_Red:
        TS_State[ts] = "1"
    elif tsColor == TS_Yellow:
        TS_State[ts] = "1"
    elif tsColor == TS_Off:
        TS_State[ts] = "0"

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
           lToStnMiles, lTripMiles, LocalLpCt, lLpCtEn, LScale, \
           mToStnMiles, mTripMiles, MainLpCt, mLpCtEn, MScale

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
        if TS_Type[7] == "":
            TS_Type[7] = " "
        f.close()
        TS_Blinker()
    except:
        filename = ""
        TrackInventoryVer = 0.0

def Save_Train_State(fN):
    global TrackStateVer, SV_State, TS_State, TD_Type, MainStation, \
           SV_Type, TS_Type, TD_Type, TrackInventoryVer, \
          mToStnMiles, mTripMiles, MainLpCt, mLpCtEn, MScale, mPtr

    # Change name of current invertory file to *.bak
    try:
        fBak = "./"+fN+".bak"
        fNew = "./"+fN+".ses"
        if os.path.exists(fBak):
            os.path.remove(fBak)
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

    # Save Train Positions and Routes
    line = ""
    f.write("Acela Route Selection\n")
    f.write(str(mPtr)+"\n")
    f.write("Direction:\n")
    f.write(Main_Dir+"\n")
    f.write("Loop Number:\n")
    f.write(str(MainLpCt)+"\n")
    f.write("Miles To Station:\n")
    f.write(str(mToStnMiles)+"\n")
    f.write("Trip Miles:\n")
    f.write(str(mTripMiles)+"\n")
    f.write("Scale:\n")
    f.write(str(MScale)+"\n\n")

    f.write("CT Route Selection\n")
    f.write(str(lPtr)+"\n")
    f.write("Direction:\n")
    f.write(Local_Dir+"\n")
    f.write("Loop Number:\n")
    f.write(str(LocalLpCt)+"\n")
    f.write("Miles To Station:\n")
    f.write(str(lToStnMiles)+"\n")
    f.write("Trip Miles:\n")
    f.write(str(lTripMiles)+"\n")
    f.write("Scale:\n")
    f.write(str(LScale)+"\n")
    f.close()

def LoadCurSession(fn):
    global TrackStateVer, SV_State, TS_Type, TS_State, TD_State, \
           mToStnMiles, mTripMiles, MainLpCt, MScale, mPtr, Main_Dir, \
           lToStnMiles, lTripMiles, LocalLpCt, LScale, lPtr, Local_Dir

    TrackStateVer = 0.0
    # filename = "Session.ses"    
    try:
        if fn == False:
            fn = "CurSession"
        f = open(fn+".ses")
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
        TS_State = line.split(", ")
        if TS_State[7] == "":
            TS_State[7] = " "

        # Acela Data
        line = lines[17].strip("\n")
        mPtr = int(line)
        line = lines[19].strip("\n")
        Main_Dir = line
        line = lines[21]
        MainLpCt = int(line)
        line = lines[23]
        mToStnMiles = int(line)
        line = lines[25]
        mTripMiles = int(line)
        line = lines[27]
        MScale = int(line)

        # CT Shore Data
        line = lines[30].strip("\n")
        lPtr = int(line)
        line = lines[32].strip("\n")
        Local_Dir = line
        line = lines[34]
        LocalLpCt = int(line)
        line = lines[36]
        lToStnMiles = int(line)
        line = lines[38]
        lTripMiles = int(line)
        line = lines[40]
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
    global SessionName
    LoadCurSession(SessionName)

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
    global lToStnMiles, lTripMiles, LocalLpCt, LScale, lPtr, Local_Dir, LocalMiles

    # Load CT Shore Start point and direction of travel
    LocalMiles = 0
    if (fFile == False):
        LocalLpCt = 0
    LocalStation = CleanCt(Local_NS[lPtr],"")
    w.ui.lblLocStaNm.setText(LocalStation)
    lTripMiles = 0
    if Local_Dir == "S":
        w.ui.lblL_L.setText("L SB")
        w.ui.lblL_R.setText("L SB")
        if lPtr>1:
            lToStnMiles = Loc_M_NS[lPtr-1]
            w.ui.lblLocal_Arriv.setText(CleanCt(Local_NS[lPtr-1],""))
            if lPtr < (len(Local_NS)-1):
                w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr+1],"y"))
            else:
                w.ui.lblLocal_Dest.setText("")
        else:
            lToStnMiles = Loc_M_NS[lPtr+1]
            w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr+1],"y"))
            w.ui.lblLocal_Arriv.setText("Arrived")
        for i in range((len(Loc_M_NS)-1)-lPtr):
            LocalMiles += Loc_M_NS[i]
        # LocalMiles = Local_M_NS[mPtr]
        item = w.ui.tblLTrip.item(0,0)
        item.setText(str(LocalMiles))
        item = w.ui.tblLTrip.item(1,0)
        item.setText(str(Loc_M_NS[mPtr]))
    else:
        w.ui.lblL_L.setText("L NB")
        w.ui.lblL_R.setText("L NB")
        if lPtr<(len(Local_NS)-2):
            w.ui.lblLocal_Arriv.setText(CleanCt(Local_NS[lPtr+1],""))
            if lPtr<(len(Local_NS)-1) :
                w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr-1],"y"))
            else:
                w.ui.lblLocal_Arriv.setText("")
        else:
            w.ui.lblLocal_Dest.setText(CleanCt(Local_NS[lPtr-1],"y"))
            w.ui.lblLocal_Arriv.setText("")
        # LocalMiles = Local_M_SN[mPtr]
        for i in range(0,lPtr):
            LocalMiles += Loc_M_SN[i]
        item = w.ui.tblLTrip.item(0,0)
        item.setText(str(LocalMiles))
        item = w.ui.tblLTrip.item(1,0)
        item.setText(str(Loc_M_SN[lPtr-1]))

def Load_Acela_Data(fFile):
    global  mToStnMiles, mTripMiles, MainLpCt, MScale, mPtr, \
            Main_Dir, MainMiles, mMilesToNext

    # Load Acela Start point and direction of travel
    MainMiles = 0
    mTripMiles = 0.0
    if (fFile == False):
        MainLpCt = 0
    #item = w.ui.tblMtoSta.item(1,0)
    #item.setText("0.0")
    if Main_Dir == "S":
        w.ui.lblM_L.setText("M SB")
        w.ui.lblM_R.setText("M SB")
        mTripMiles = 0
        if mPtr>1:
            mToStnMiles = Main_M_NS[mPtr+1]
            w.ui.lblMain_Arriv.setText(Main_NS[mPtr-1])
            if mPtr < (len(Main_NS)-1):
                w.ui.lblMain_Dest.setText(Main_NS[mPtr+1])
            else:
                w.ui.lblMain_Dest.setText("")
        else:
            mToStnMiles = Main_M_NS[mPtr+1]
            w.ui.lblMain_Dest.setText(Main_NS[mPtr+1])
            w.ui.lblMain_Arriv.setText("")
        # MainMiles = Main_M_NS[mPtr]
        for i in range((len(Main_M_NS)-1)-mPtr):
            MainMiles += Main_M_NS[i]
        item = w.ui.tblMTrip.item(0,0)
        item.setText(str(MainMiles))
        item = w.ui.tblMTrip.item(1,0)
        item.setText(str(Main_M_NS[mPtr]))
    else:
        w.ui.lblM_L.setText("L NB")
        w.ui.lblM_R.setText("L NB")
        mTripMiles = 0.0
        mMilesToNext = 0.0
        if mPtr<(len(Main_NS)-2):
            mToStnMiles = Main_M_SN[mPtr-1]
            w.ui.lblMain_Arriv.setText(Main_NS[mPtr+1])
            if mPtr<(len(Main_NS)-1) :
                w.ui.lblMain_Dest.setText(Main_NS[mPtr-1])
                mMilesToNext = Main_M_NS[mPtr]
            else:
                w.ui.lblMain_Arriv.setText("")
        else:
            mToStnMiles = Main_M_SN[mPtr-1]
            w.ui.lblMain_Dest.setText(Main_NS[mPtr-1])
            w.ui.lblMain_Arriv.setText("")
        # MainMiles = Main_M_SN[mPtr]
        for i in range(0,mPtr):
            MainMiles += Main_M_SN[i]
        item = w.ui.tblMTrip.item(0,1)
        item.setText(str(MainMiles))
        item = w.ui.tblMTrip.item(1,1)
        item.setText(str(mMilesToNext))

        item = w.ui.tblMtoSta.item(0,1)
        item.setText(str("%.2f" % mTripMiles))
        item = w.ui.tblMtoSta.item(1,1)
        item.setText(str("%.2f" % mToStnMiles))



class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_mwinAI_Train()
        self.ui.setupUi(self)

        Load_Track_Inventory()

        def CT_Shore():
            global lPtr, Local_Dir, LScale
            dlgwin = QDialog()
            dlgC = Ui_dlgCTStPt()
            dlgC.setupUi(dlgwin)
            dlgC.cbxCtShorStartPt.addItems(Local_NS)
            if dlgwin.exec_():
                lPtr = dlgC.cbxCtShorStartPt.currentIndex()
                Local_Dir = dlgC.cbxCtShoreDir.currentText()[0]
                LScale = dlgC.sbxScale.value()
                Load_CT_Data(False)

        def AcelaStPt():
            global mPtr, Main_Dir, MScale

            dlgwin = QDialog()
            dlgA = Ui_dlgAcelaStPt()
            dlgA.setupUi(dlgwin)
            dlgA.cbxAcelaStartPt.addItems(Main_NS)
            if dlgwin.exec_():
                mPtr = dlgA.cbxAcelaStartPt.currentIndex()
                Main_Dir = dlgA.cbxAcelaDir.currentText()[0]
                MScale = dlgA.sbxScale.value()
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

        def CloseTrainAI():
            global SessionName
            Save_Train_State(SessionName)
            self.close()

        self.ui.actionAcela.triggered.connect(AcelaStPt)
        self.ui.actionCT_Shore.triggered.connect(CT_Shore)
        # self.ui.actionStart_Acela.triggered.connect(Start_Acela)
        # self.ui.actionStart_CT_Shore.triggered.connect(Start_CTShore)
        # self.ui.actionStart_Both.triggered.connnect(Start_Both)
        # # self.ui.actionPreferences.triggered.connect(self.Preferences())
        self.ui.actionQuit.triggered.connect(CloseTrainAI)
        self.ui.actionSavCurSession.triggered.connect(SaveSession)
        self.ui.actionSave_Session_as.triggered.connect(SaveSessionAs)
        self.ui.actionLoad_Last_Session.triggered.connect(LoadCurSession)
        self.ui.actionLoad_Session.triggered.connect(LoadSessionAs)

        self.TTimer = QTimer()
        self.TTimer.timeout.connect(TS_Blinker)
        self.TTimer.start(50)

        self.DTimer = QTimer()
        self.DTimer.timeout.connect(ReadDetectors)
        self.DTimer.start(50)

        # self.runTimer = QTimer()
        # self.runTimer.timeout.connect(LoopRoutines)
        # self.runTimer.start(1000)

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())

    # mwinAI_Train = QtWidgets.QMainWindow()
    # ui = Ui_mwinAI_Train()
    # ui.setupUi(mwinAI_Train)
    # mwinAI_Train.show()
    # sys.exit(app.exec_())
   