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

Required libraries to import: pyautogui, cv2, numpy, time, msvcrt, os, pathlib, threading

You may need to use the terminal and pip to install these libraries. Try these steps:
    1) pip install pip (only do once)
    2) pip install *library name here* (once per library)
    * Libraries that require pip: cv2 (library is opencv-python), and pyautogui (library is pyautogui)
    * You will also need Pillow, it's a dependency for opencv
    https://pypi.org/project/opencv-python/
    https://pypi.org/project/PyAutoGUI/

    "pip install opencv-python"
    "pip install pyautogui"
    "pip install Pillow"
    "pip install numpy"

NOTE: I have made the filepath system dynamic. Logic and requirements as follows:
    1) Your script (.py file) may be in any folder you choose!
    2) Your target folder (.png images of targets) must be named "targets" and must be inside the script folder
        ex. myFolder/script.py, along with myFolder/targets/image.png are valid paths.
        ex. myFolder/script.py, along with myFolder/image.png are NOT valid because we have no embedded targets folder
    3) The desktop screenshot will be automatically placed inside the same folder as your script (not targets folder)

NOTE: This program has an accompanying config file which can be used to enable and disable different target images
    By disabling a target image that a user knows they don't want to track some processing time can be saved.
    The config file has comment lines which are prefixed with a '#', these lines will be ignored.
    The config file uses 1 to enable tracking for a particular alert and 0 to disable tracking for any given alert
    Alerts are given shorthand names in the config file to save space but the names are detailed enough to explain
    PLEASE ensure that any config items added to the file match the name of their respective target image in the target
        folder.

NOTES FOR BRYCE:
    1) current state of script starts looping the moment it's opened, keep this in mind
    2) alerts are removed once found for the next 300 seconds
    3) if an item wants to add to the tracking list we must:
        a) add its image to the "targets" folder
        b) add its filename to config.cfg as "filename=1" where 1 is active and 0 is inactive
        c) note that the cooldowns do not change these config file values mid-execution
    4) for cyber reasons, we should delete the screenshot of the desktop from our folder once finished
    #  if you don't have the filepath stored locally you can use this to find the path THEN delete it:
    scriptPath = __file__  # get the file path for this program using a built-in command
    path = pathlib.Path(scriptPath)  # converting the file path to a pathlib type for methods
    pathScreenshot = path.parent  # get the filepath without the script at the end of it (parent folder)
    pathScreenshot = pathScreenshot.joinpath(pathScreenshot,
                                           'screenshot1.png')  # append the screenshot name to the path
    pathScreenshot = pathlib.PureWindowsPath(
    pathScreenshot).as_posix()  # convert the screenshot filepath to Windows-style for the os.remove command.
    #  by here we should have the filepath to the screenshot assuming it's in the same folder as the scripts
    os.remove(pathScreenshot)  # delete the screenshot we took

    5) feel free to delete all the print statements from this code if you don't need them, they're here for clarity

"""
from ast import If  # for WindowsProcess.py

import pathlib
import os
import time

import pyautogui  # take screenshots
import cv2  # display images
import numpy as np  # math work
from time import process_time_ns  # needed for time estimate
import threading  # threading used for event cooldown timer handling

# creating variables for lists of processes
ulist = []  # create variable for user list of values to check
initial_count = []  # variable for the initial list of processes to check
current_count = []  # variable for the current list of processes to check
process_time = 5  # variable to set the time between process checks in seconds


# ^^^ Global Variables for the WindowsProcess.py section of the code (see Github for more)


# Function to create list of processes running on host machine
def process_read():
    process_count = {}  # create variable for processes to be counted
    process_current = os.popen('wmic process get description').read()  # read list of current processes
    process_list = process_current.strip().split('\n')[1:]  # remove header line and split by newline
    process_set = set(process_list)  # convert to set to remove duplicates
    # loop to find occurrences of each process
    for process in process_set:  # iterate through 'process set' array
        count = process_list.count(process)  # count the number of processes
        process_count[process] = count  # create dictionary of processes

    process_output = [f"{process} ({count})".strip() for process, count in
                      process_count.items()]  # put the contents of the previous loop together
    return process_output  # return the list of processes dictionary


# Compare the processes in the config file to the processes recorded running on the machine
def count_processes(ulist, process_output):
    entry_counts = {}  # create variable for number of entries
    for process in ulist:
        count = 0
        for output in process_output:
            if process.lower() in output.lower():
                count += int(output.split("(")[1].split(")")[0])
        entry_counts[process] = count
    return entry_counts


def enable_alert():  # if an alert was found it needs to be disabled for 300 seconds. This is how we enable it after
    global finalFileList  # do this so that the main script sees the change to this list
    finalFileList.append(cooldownList[0])  # while globals can be risky these have very specific purposes that are safe
    del cooldownList[0]  # delete the first item from the list since this is the oldest alert on CD
    # this will continue to work fine unless we design a secondary way to place or remove alerts from cooldown (not rn)


# this function processes one target file at a time against our desktop screenshot and then displays an image if it hit
def scanimage(filepath):  # takes a windows-style filepath to a target image as input and searches for it in img_gray
    counter = 0  # start a counter for use in the following loop:
    target_img = cv2.imread(filepath, 0)  # read the target img using the openCV read command
    w, h = target_img.shape[::-1]  # get info on target img and convert to a width and height value
    res = cv2.matchTemplate(img_gray, target_img, cv2.TM_CCOEFF_NORMED)  # check for matches of target on
    # matchTemplate returns a set of confidence values based on image size
    threshold = 0.8  # threshold for res values that we care about (if 80% + confident, it's a hit right now).
    loc = np.where(res >= threshold)  # this will only care about hits over our threshold
    for pt in zip(*loc[::-1]):  # start the detection loop which paints rectangles on our matches
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)  # draw a rectangle where the hit is
        confidence = res[pt[1]][pt[0]]  # res holds confidence levels across the image
        print('\n\n*****************************************************')
        print('match with conf = ', confidence)  # show confidence to console (can remove if wanted)
        print("filepath of image match = ", pathlib.Path(filepath))
        if finalFileList.__contains__(pathlib.Path(filepath)):  # this is b/c sometimes an alert is already cleared
            finalFileList.remove(pathlib.Path(filepath))  # the type casting is very important, must be pathlib path!
        # remove this filepath from the finalFileList temporarily (on cooldown)
        global cooldownList  # declare global before first use, must do in Python for global varbs
        cooldownList.append(pathlib.Path(filepath))  # add any cooldown filepaths to a cooldown list for storage
        global cooldownCount  # edit cooldownCount across entire script, so we can use enableAlert function
        timer.insert(cooldownCount, threading.Timer(300.0, enable_alert))
        # may need to set multiple timers, using a list
        # set a 300-second timer then enable the alert again
        timer[cooldownCount].start()  # list of timers but only start timing the current one here
        cooldownCount = cooldownCount + 1  # increment once per item on CD
        # starting the timer above , note that timer.cancel() can stop a timer if it hasn't gone off yet
        # cv2.imshow(' ', img)  # display the image with our "confidence" rectangles on it
        print("filelist after cooldown: ", finalFileList)
        print('*****************************************************\n\n')
        counter = counter + 1  # this counter just shows how many times we've looped through this block (once per match)
    # print('num of loop iterations: ', counter)


exitLoop = 0  # this loop starts once the user has pressed g at least once
cooldownCount = 0  # how many items are on cooldown right now?
t1_start = process_time_ns()  # recording elapsed time so we know what to expect

scriptPath = __file__  # get the file path for this program
path = pathlib.Path(scriptPath)  # converting the file path to a pathlib type for methods
pathHead = path.parent  # get the filepath without the script at the end of it (parent folder)
pathScreenshot = pathHead  # get a spare copy to use for our desktop screenshot filepath later
pathConfig = pathHead  # get another spare copy for our config filepath later
pathConfig = pathScreenshot.joinpath(pathScreenshot, 'config.txt')  # append the parent path with config file
pathScreenshot = pathScreenshot.joinpath(pathScreenshot, 'screenshot1.png')  # append the screenshot name to the path
pathScreenshot = pathlib.PureWindowsPath(pathScreenshot).as_posix()  # convert the screenshot filepath to Windows-style
pathHead = pathHead.joinpath(pathHead, 'targets')  # append "targets" to the end since this is where we keep images
fileList = os.listdir(pathHead)  # this holds all filepaths for files inside the "target" folder

config = open(pathConfig, "r")  # open the config file in reading more
keeperList = []  # list of pictures we're keeping based config file, feeds into finalFileList
finalFileList = []  # final list of files we're tracking from target folder and config file
cooldownList = []  # list of filenames that are on cooldown (no track b/c recent hit)
timer = []  # a list of timers which are 300 seconds and call enable_alert when complete. 1 timer per alert on cooldown

single = config.readline()  # get an initial line to begin the while loop. Make sure there are no blank lines

# NOTE TO DISCUSS WITH RYAN: current config file cannot have spaces... could add something to manipulate them
#   are spaces needed for his process tracking?
while single != '':  # while we're not at the end of the file:
    single = single.strip()  # remove \n from the end of each line for better analysis. This also removes whitespaces
    if not single.__contains__("#") and not single.__contains__("*"):
        #  If the line has a # it's a comment, and if it has a * it's for the Windows Process tracker (4 lines down)
        divided = single.split("=")  # dividing at the '=', so we can check the value after the '=' (0 or 1?)
        if divided[1] == '1':  # if the second part is 1, we want to track this alert
            keeperList.append(divided[0])  # add any items with a 1 to the keeper list (targets to track)
    if single.startswith('*'):  # check for process character (*)
        ulist.append(single.lstrip('*').strip())  # format output and add to ulist
    single = config.readline()  # read a line into the file for processing..., also last line of while loop
config.close()  # close out of the config file since it's good practice to do this once finished.

fileCounter = 0  # using this in the following loop for indexing
for f in fileList:  # for the number of items in fileList
    g = f.split('.')  # split at the filetype '.' to keep only the file's name.

    if g[0] in keeperList:  # if file in targets was found in the keeperList (items we've marked in config.txt)...
        h = pathlib.Path(f).joinpath(pathHead, f)  # ex. join directory path with stopsign.png for full path to image
        # h = pathlib.PureWindowsPath(h.as_posix())  # changing slashes for later use with windows libraries
        #  The pathlib library works with Linux-style paths, but we need windows-style paths for scanimage()
        finalFileList.append(h)  # add all of our final filepaths to a list called finalFileList

# print("final file list: ", finalFileList)  # this list is all targets we will actually track during program loop

initial_count = count_processes(ulist, process_read())  # store the initial count of running processes
print(initial_count)
reset_count = 0  # end of WindowsProcess.py setup before "main" / infinite loop

while 1:  # wait for user to press 'g' before we begin checking for alert matches
    print('entering program loop')
    #  Start of WindowsProcess.py infinite loop segment
    current_count = count_processes(ulist, process_read())  # store the current count of running processes
    if initial_count == current_count:  # check for differences
        print(current_count)  # print current processes
    elif reset_count == 0:  # check if reset is complete
        print(current_count)  # print current processes
        print('output to API')  # "output to API"
        reset_count = 300  # Set Reset Counter to x * process_time
    else:
        print(current_count)  # print current processes
        reset_count = reset_count - 1  # iterate counter down by 1
    #  time.sleep(process_time)
    #  End of WindowsProcess.py infinite loop segment
    #  Start of DetectImage.py infinite loop segment
    screenshot1 = pyautogui.screenshot()  # take a screenshot of current screen an save as 'screenshot1.png')
    screenshot1.save(pathScreenshot)
    img = cv2.imread(pathScreenshot)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Screenshot", img)
    fileCounter = 0
    for f in finalFileList:  # for every item that made it to the final file list (keepers)
        print("scanimage param:", finalFileList[fileCounter])
        scanimage(str(finalFileList[fileCounter]))  # hard casting to a string here to ensure it fits imread()
        fileCounter = fileCounter + 1  # increment to scan the next image in the list
        # items can be removed or added from this list to enable and disable alert tracking.
        # cv2.waitKey(0)  # pause the program while the image is displayed
    os.remove(pathScreenshot)  # delete the screenshot we took
    time.sleep(1)  # pause for a moment before checking a new screenshot for resource conservation purposes.

    # can remove if desired or add more delay, doesn't matter but note that currently 1 second per sweep of image
