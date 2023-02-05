# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:11:10 2023

@author: Ben
filename: detectImage.py
description: Checking to see if we can spot an image when it is part of a pic
date: 1/25/23

Required libraries to import: pyautogui, cv2, numpy, time, msvcrt

You may need to use the terminal and pip to install these libraries. Try these steps:
    1) pip install pip (only do once)
    2) pip install *library name here* (once per library)

Current program flow: wait for user to press 'g' key, then begin scanning for the stopsign.jpg picture

Once found it will open and program will stop.

NOTE: If the image with the target highlighted is closed it will reappear for now.
    I plan on fixing this later, so it doesn't reopen.

NOTE: I have some filepaths in here specific to my system, they'll likely give you an error Syema.
    Change these so you can test better, don't worry about overwriting them. I'll make a file for them later

Program can be stopped early by pressing the 's' key
"""

import pyautogui  # take screenshots
import cv2  # display images
import numpy as np  # math work
from time import process_time_ns  # needed for time estimate
import msvcrt  # keyboard input and event handling

print('Press g to begin scanning screen for alerts\nPress s to stop')

exitLoop = 0  # this loop starts once the user has pressed g at least once
t1_start = process_time_ns()  # recording elapsed time so we know what to expect

while 1:  # wait for user to press 'g' before we begin checking for alert matches

    pressedKey = msvcrt.getch()  # keep a variable on standby for key presses

    if pressedKey == b's':  # if the user wants to stop before entering the loop it'll go here

        print('exiting program')
        t1_stop = process_time_ns()
        print("Elapsed time during the whole program in nanoseconds:", t1_stop - t1_start)
        print("Elapsed time during the whole program in seconds:", (t1_stop - t1_start) / 1000000000)
        quit()

    elif pressedKey == b'g':  # if the user wants to enter the program we will go here

        print('entering program loop')
        while exitLoop == 0:  # while the exit value is still 0, keep looping (until they press 's')

            if msvcrt.kbhit():
                pressedKey2 = msvcrt.getch()  # keep a variable on standby for key presses
                if pressedKey2 == b's':  # exit here
                    print('exiting program')
                    t1_stop = process_time_ns()
                    print("Elapsed time during the whole program in nanoseconds:", t1_stop - t1_start)
                    print("Elapsed time during the whole program in seconds:", (t1_stop - t1_start) / 1000000000)
                    quit()  # close out on 's' key

            screenshot1 = pyautogui.screenshot()  # take a screenshot of current screen an save as 'screenshot1.png')
            screenshot1.save(r'C:\Users\Ben\Python_Projects\screenshot1.png')

            img = cv2.imread('C:/Users/Ben/Python_Projects/screenshot1.png')
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("Screenshot", img)

            target_img = cv2.imread('C:/Users/Ben/Python_Projects/targets/stopsign.png', 0)  # read the target img

            w, h = target_img.shape[::-1]  # get info on target img

            res = cv2.matchTemplate(img_gray, target_img, cv2.TM_CCOEFF_NORMED)  # check for matches of target on
            # screenshot

            threshold = 0.8  # confidence threshold, lower for more "hits" (some may be wrong), raise for only
            # perfect matches
            # min is 0.01, max is 1.0

            loc = np.where(res >= threshold) # this will only care about hits over our threshold

            counter = 0 # start a counter for use in the following loop:

            for pt in zip(*loc[::-1]): # this loop basically filters through every possible hit at our conf or higher
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2) # draw a rectangle where the hit is
                confidence = res[pt[1]][pt[0]]
                print('conf = ', confidence) # show confidence to console (can remove if wanted)
                cv2.imshow(' ', img) # display the image with our "confidence" rectangles on it
                counter = counter + 1

            print('num of loop iterations: ', counter)

            # print('loc = ', loc)
            # print('zip = ', zip(*loc[::-1]))

            # # with the method used, the date in res are top left pixel coords
            # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # top_left = max_loc

            # # if we add to it the width and height of the target, then we get the bbox.
            # bottom_right = (top_left[0] + w, top_left[1] + h)

            # cv2.rectangle(img,top_left, bottom_right, 255, 2)
            # cv2.imshow('', img)

            cv2.waitKey(0)  # pause the program while the image is displayed
    else:  # alt flow if wrong key is pressed
        print('please enter "s" or "g"')
        print('you pressed: ')
        print(pressedKey)
