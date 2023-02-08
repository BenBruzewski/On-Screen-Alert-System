# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:11:10 2023

@author: Ben
filename: detectImage.py
description:
    This program uses image recognition techniques to match "target" images to a desktop screenshot
    the function starts when the user presses the 'g' key in their console (in pycharm, do this at bottom of IDE)
        NOTE pycharm: goto Run --> Edit Configurations --> Emulate Terminal in Output Console to enable this feature!!!
        NOTE For VSCode or Spyder, Spyder takes console input by default in terminal, VSCode I believe does too.
    a function named scanimage() takes one filepath to a "target" image at a time and compares it to the screenshot
    if a match is found, a pop-up of the image with a rectangle showing the match will appear.
        if this pop-up is closed, the program will continue searching for another match (close alert before this!)
    if no match is found, the loop will continue searching until the user requests to stop via the 's' key

date: 2/8/23

Required libraries to import: pyautogui, cv2, numpy, time, msvcrt, os, pathlib

You may need to use the terminal and pip to install these libraries. Try these steps:
    1) pip install pip (only do once)
    2) pip install *library name here* (once per library)

NOTE: I have made the filepath system dynamic. Logic and requirements as follows:
    1) Your script (.py file) may be in any folder you choose!
    2) Your target folder (.png images of targets) must be named "targets" and must be inside the script folder
        ex. myFolder/script.py, along with myFolder/targets/image.png are valid paths.
        ex. myFolder/script.py, along with myFolder/image.png are NOT valid because we have no embedded targets folder
    3) The desktop screenshot will be automatically placed inside the same folder as your script (not targets folder)

"""
import pathlib
import os
import pyautogui  # take screenshots
import cv2  # display images
import numpy as np  # math work
from time import process_time_ns  # needed for time estimate
import msvcrt  # keyboard input and event handling


# this function processes one target file at a time against our desktop screenshot and then displays an image if it hit
def scanimage(filepath):  # takes a windows-style filepath to a target image as input and searches for it in img_gray
    counter = 0  # start a counter for use in the following loop:
    target_img = cv2.imread(filepath, 0)  # read the target img
    w, h = target_img.shape[::-1]  # get info on target img
    res = cv2.matchTemplate(img_gray, target_img, cv2.TM_CCOEFF_NORMED)  # check for matches of target on
    threshold = 0.8
    loc = np.where(res >= threshold)  # this will only care about hits over our threshold
    for pt in zip(*loc[::-1]):  # start the detection loop which paints rectangles on our matches
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)  # draw a rectangle where the hit is
        confidence = res[pt[1]][pt[0]]
        print('match with conf = ', confidence)  # show confidence to console (can remove if wanted)
        cv2.imshow(' ', img)  # display the image with our "confidence" rectangles on it
        counter = counter + 1
    print('num of loop iterations: ', counter)


print('Press g to begin scanning screen for alerts\nPress s to stop')

exitLoop = 0  # this loop starts once the user has pressed g at least once
t1_start = process_time_ns()  # recording elapsed time so we know what to expect

scriptPath = __file__  # get the file path for this program
path = pathlib.Path(scriptPath)  # converting the file path to a pathlib type for methods
pathHead = path.parent  # get the filepath without the script at the end of it (parent folder)
pathScreenshot = pathHead  # get a spare copy to use for our desktop screenshot filepath later
pathScreenshot = pathScreenshot.joinpath(pathScreenshot, 'screenshot1.png')  # append the screenshot name to the path
pathScreenshot = pathlib.PureWindowsPath(pathScreenshot).as_posix()  # convert the screenshot filepath to Windows-style
pathHead = pathHead.joinpath(pathHead, 'targets')  # append "targets" to the end since this is where we keep images
fileList = os.listdir(pathHead)  # this holds all filepaths for files inside the "target" folder
fileCounter = 0  # using this in the following loop for indexing
for f in fileList:  # for the number of items in fileList
    fileList[fileCounter] = pathlib.Path(fileList[fileCounter]).joinpath(pathHead, fileList[fileCounter])
    fileList[fileCounter] = pathlib.PureWindowsPath(fileList[fileCounter]).as_posix()  # convert to Windows-type paths
    #  modify each item in fileList to become a pathlib object, so we can join it with its full parent path
    fileCounter = fileCounter + 1  # move to the next item in the folder so that we can process each existing file

print(fileList[0])  # at this point we have the FULL filepath to each target image dynamically

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
            screenshot1.save(pathScreenshot)

            img = cv2.imread(pathScreenshot)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("Screenshot", img)

            fileCounter = 0
            for f in fileList:
                scanimage(fileList[fileCounter])
                fileCounter = fileCounter + 1

            cv2.waitKey(0)  # pause the program while the image is displayed
    else:  # alt flow if wrong key is pressed
        print('please enter "s" or "g"')
        print('you pressed: ')
        print(pressedKey)
