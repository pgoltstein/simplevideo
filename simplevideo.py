#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple script to record webcam video

Created on Mon 7 Dec 2020
@author: pgoltstein
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# User settings
video_resolution = (640,480) # (x,y)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
import cv2
import numpy as np
import sys, os, time, datetime
from sys import platform as _platform
import argparse

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Arguments
parser = argparse.ArgumentParser(description = "Runs a webcam continuously, stops at escape. (written by Pieter Goltstein - December 2020)")

parser.add_argument('-n','--filename', type=str, default="", help= 'Filename-stem for storing video (date and time will be added automatically)')
args = parser.parse_args()
filename = args.filename

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Detect operating system
if "linux" in _platform.lower():
   OS = "linux" # linux
   save_location = "/tmp"
elif "darwin" in _platform.lower():
   OS = "macosx" # MAC OS X
   save_location = "/Users/pgoltstein/figures"
elif "win" in _platform.lower():
   OS = "windows" # Windows
   save_location = "C:/Videos"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Open webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, video_resolution[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, video_resolution[1])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize window and buffer
cv2.imshow('Preview',np.zeros( (video_resolution[0], video_resolution[1]), dtype=np.uint8 ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Configure location of timestamp
font                   = cv2.FONT_HERSHEY_COMPLEX_SMALL
bottomLeftCornerOfText = (10,video_resolution[1]-10)
fontScale              = 1
fontColor              = (0,0,255)
lineThickness          = 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Location and name of file
date_time_path = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
save_path = os.path.join(save_location,filename+"-"+date_time_path)

# Define the codec and create VideoWriter object
if OS == "macosx":
    video_file_name = save_path+'.mov'
    print("Creating file: {}".format(video_file_name))
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0, (video_resolution[0],video_resolution[1]) )
elif OS == "windows":
    video_file_name = save_path+'.avi'
    print("Creating file: {}".format(video_file_name))
    fourcc = cv2.VideoWriter_fourcc(*'divx')
    video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0, (video_resolution[0],video_resolution[1]) )
elif OS == "linux":
    video_file_name = save_path+'.avi'
    print("Creating file: {}".format(video_file_name))
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0, (video_resolution[0],video_resolution[1]) )

# Capture and show frame-by-frame
print("Starting recording...")
frame_counter = 0
while True:

    # Read frame
    ret, frame = cap.read()
    frame_counter += 1

    # Make timestamp + frame counter
    date_time = datetime.datetime.now().strftime("%d %b %Y - %H:%M:%S")
    date_time += " - frame {:6d}".format(frame_counter)

    # Save the frame
    cv2.putText(frame, date_time, bottomLeftCornerOfText, font, fontScale, fontColor, lineThickness)
    video_object.write(frame)

    # Show on screen
    cv2.imshow('Preview',frame)

    # Quit if escape pressed
    try:
        k = cv2.waitKey(1) & 0xff
        if k == 27: break
    except:
        pass

# Close file if saving is finished
video_object.release()
print(" -> done, wrote {} frames to file: {}".format( frame_counter, video_file_name ))

# Release webcam and close window
cv2.destroyAllWindows()
