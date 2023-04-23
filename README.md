# MWL_Sensorlab
###
This repository contains:
1. Circuitpython Program to collect sensordata of three sensors on a Maker Pi Pico
2. Python program to run a Sternberg memory task, collect data and merge it with the data comming in from the Maker Pi Pico
3. The same thing for a second task, the Restaurant Task

###
All the code is elaborately commented and a video is provided explaining the code for beginners looking to work with the YLAB 
and implementing multiple sensors and a direct transfer of sensor data to the PC

###
The most important things to get this code running quickly will be outlined:

# Setting up the board
You will need to have the YLAB libraries installed on your board, which can be found here:
https://github.com/schmettow/YLab

# Sendsor data
Check that the pins that you have connected your sensors to correspond with the pins that are used in the code.
Furthermore you need to create a boot.py file on your Maker Pi Pico which enabled usb_cdc serial connection. Create the file and paste this code into it:
import usb_cdc
usb_cdc.enable(console=True, data=True)

# Sternberg and Restaurant Task:
Set the COM (portVar) to the Com port which you are using to communicate with the Maker Pi Pico. 
You can find this out by opening your device manager (Windows Key + x -> Device manager) and then opening the Ports (COM & LPT) menu.
There you should see two instances. Usually the first (lower number) is the instance that is used for the communication of the Console.
The second one (higher) is the port which is used to send data from the Maker Pi Pico to the PC. Use this as portVar in the files of the tasks.

Furthermore, you will need to specifiy the directory in which you are running the files in the datamerge function far down in the code.
Look at the path where you are currently running the program of the task, as this is also where the excel files with the data will be saved.

### A video guide going through the code and roughly outlining the key functions and variables that can be manipulated can be found here:
-Work in Progress-
