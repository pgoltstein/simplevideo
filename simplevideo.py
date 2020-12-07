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
buffer_size = 60
motion_compare_past = 10

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
import cv2
import numpy as np
import sys, os, time, datetime
from sys import platform as _platform
import argparse

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Arguments
parser = argparse.ArgumentParser( \
    description = \
        "Runs a webcam continuously. " + \
        "(written by Pieter Goltstein - December 2020)")

parser.add_argument('-n','--filename', type=str, default="",
                    help= 'Filename for storing video')
args = parser.parse_args()
filename = args.filename

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Detect operating system
if "linux" in _platform.lower():
   OS = "linux" # linux
   save_location = "C:/Videos"
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
cv2.imshow('Preview',np.zeros( (video_resolution[0], video_resolution[1]), dtype=int ))

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
    print("Detected motion, creating file: {}".format(video_file_name))
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0,
        (video_resolution[0],video_resolution[1]) )
elif OS == "windows":
    video_file_name = save_path+'.avi'
    print("Detected motion, creating file: {}".format(video_file_name))
    fourcc = cv2.VideoWriter_fourcc(*'divx')
    video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0,
        (video_resolution[0],video_resolution[1]) )
elif OS == "linux":
    video_file_name = save_path+'.avi'
    print("Detected motion, creating file: {}".format(video_file_name))
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0,
        (video_resolution[0],video_resolution[1]) )

# Capture and show frame-by-frame
print("Starting recording...")
while True:

    # Read frame
    ret, frame = cap.read()
    frame_counter += 1

    # Make timestamp
    date_time = datetime.datetime.now().strftime("%d %b %Y - %H:%M:%S")

    # Save the frame
    cv2.putText(frame, date_time, bottomLeftCornerOfText, font, fontScale, fontColor, lineThickness)
    video_object.write(frame)
    write_counter += 1
    save_img -= 1

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
print(" -> done, wrote to file: {}".format(video_file_name))

# Release webcam and close window
cv2.destroyAllWindows()
