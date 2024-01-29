# Latest Update

Version 0.1.1
Adding Speed and Motion Direction routines

# Introduction

This project simulates Acela (Boston to Washington, DC with stops along the way) and the CT Shoreline (New London to Stamford) routes as represented in a Lego train setup with Acela as the outer loop and CT Shoreline as the local loop. The goal is eventually to control the trains using Bluetooth autonomously. Currently using Raspberry Pi 4 (switching to Raspberry Pi 5) to control the hardware (switches, signal lights, detectors) autonomously but train power is set manually via Lego Train Engineer or remote controllers. 

![IMG_0090](https://user-images.githubusercontent.com/23269355/162502642-ce1c6b58-4e51-4ca6-b9ed-cd489883c7f7.jpg)

## Video of Trains and GUI
[![Video of Trains and GUI](http://img.youtube.com/vi/ESV82uW2rAY)](https://youtu.be/ESV82uW2rAY "Video of Trains and GUI")

# Hardware List

* Raspberry Pi 4 Model B
    * Two display outputs
    * 8 GB RAM
    * 512 GB SD card for OS
* Adafruit 16-channel 12-bit PWM/Servo Shield - I2C interface
    * for switches and booms
* 2x AB Electronics IO Pi Plus
    * one half board for 16 bits of detectors
    * one half board plus one full board for signal lights (24 signals total)
* custom board provides 3-pin (5V+, GND, signal) for the detectors, from 
    * ideally a custom PC board would be made to allow for 3 pin servo-style connector
Switches/booms come off of PWM/Servo Shield (booms have the boom and boom light from TrixBrix)
Detectors come off of the custom board

# Setup
1. Raspberry Pi
    1. Configure Raspberry Pi
    2. Setup Adafruit board (including I2C)
        Separate 5V supply
    3. Load the module files for the AB Electronics IO Pi Plus boards
       uses Terminal
    4. Wire the top board (custom board)
3. Lego
    1. Build the track layout
    2. Add switches, detectors, lights
4. Configure Train_inventory.txt file using Train_Hardware_Test_and_Setup.py and GUI (Configurator.ui)
    * Signals
    * Switches
    * Detectors
5. Run Train_AI.py (derived from AI_Window.ui by convert_ui_to_pi.text)
