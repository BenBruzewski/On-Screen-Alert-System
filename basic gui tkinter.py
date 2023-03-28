import tkinter as tk
from configparser import ConfigParser
from ast import If

import pathlib
import os
import time

import win32gui
import win32ui
import win32con
import win32api
import cv2  # display images
import numpy as np  # math work
from time import process_time_ns  # needed for time estimate
import threading  # threading used for event cooldown timer handling

# create the main window and its dimensions
window = tk.Tk()
window.title("On Screen Alert System")
window.configure(background="white") # this background can accept hexRGB values (eg. #6FAFE7)
window.minsize(900, 600)
window.maxsize(900, 600)
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("900x600+%d+%d" % ((w/2)-450, (h/2)-300)) # starting dims and x/y coords
pNum = "-"
# create the pop-up window and its dimensions
global runningWindow
runningWindow = tk.Toplevel()
runningWindow.minsize(400,400)
runningWindow.maxsize(400,400)
runningWindow.title("OSAS is running...")
runningWindow.configure(background="grey")
runningWindow.geometry("400x400+%d+%d" % ((w/2)-200, (h/2)-300))
runningWindow.withdraw()
# create the configparsing object
confObj = ConfigParser()

# creating variables for lists of processes
ulist = []  # create variable for user list of values to check
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
finalFileList = []  # final list of files we're tracking from target folder and config file
cooldownList = []  # list of filenames that are on cooldown (no track b/c recent hit)
timer = []  # a list of timers which are 300 seconds and call enable_alert when complete. 1 timer per alert on cooldown

# ^^^ Global Variables for the WindowsProcess.py section of the code (see Github for more)


def window_capture():
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()

    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]

    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    im = saveBitMap.GetBitmapBits(True)  # Tried False also
    img = np.frombuffer(im, dtype=np.uint8).reshape((h, w, 4))

    cv2.imwrite("screenshot1.png", img)

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
    target_img = cv2.imread(filepath, 0)  # read the target img using the openCV read command
    w, h = target_img.shape[::-1]  # get info on target img and convert to a width and height value
    res = cv2.matchTemplate(img_gray, target_img, cv2.TM_CCOEFF_NORMED)  # check for matches of target on
    # matchTemplate returns a set of confidence values based on image size
    threshold = 0.75  # threshold for res values that we care about (if 80% + confident, it's a hit right now).
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
        break

# handler to accept user's update from phone number text box
def handle_pNum_update_press():
    pNum = phoneEntry.get()
    if(len(pNum) != 10):
        outVal.configure(text="Invalid Phone #. Please use 10 digits")
    else:
        pNum = pNum[:3] + "-" + pNum[3:6] + "-" + pNum[6:]
        outVal.configure(text=pNum)

# currently debugs output into terminal
def handle_button_press():
    # temporary output showing what is set up during the "running" portion of the GUI
    runPhoneLabel.configure(text=outVal.cget("text"))
    boxVals = [discCallBox.get(), discCallHalfBox.get(), discTextBox.get(), fireWBox.get(), dotaBox.get(), lolBox.get(), stopBox.get()]
    runCB2Label.configure(text="%d, %d, %d, %d, %d, %d, %d" % (boxVals[0], boxVals[1], boxVals[2], boxVals[3], boxVals[4], boxVals[5], boxVals[6]))
    # modify the config file
    msg = ""
    with open("config.txt", "r") as f:
        msg = f.readlines()
    newMsg = ""
    count = 0
    for x in msg:
        if x[0] != "#":
            if x[0] != "*":
                val = 0
                line = ""
                for i in x:
                    if i == "=":
                        val = 1
                        line += "="
                    if val == 1:
                        i = str(boxVals[count])
                        count+=1
                        line += i
                        break
                    line += i
                newMsg += line + "\n"
            else:
                newMsg += x
        else:
            newMsg += x
    with open("config.txt", "w") as f:
        f.write(newMsg)

    window.withdraw()
    runningWindow.deiconify()

    config = open(pathConfig, "r")  # open the config file in reading more
    single = config.readline()  # get an initial line to begin the while loop. Make sure there are no blank lines
    keeperList = []  # list of pictures we're keeping based config file, feeds into finalFileList

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

    for f in fileList:  # for the number of items in fileList
        g = f.split('.')  # split at the filetype '.' to keep only the file's name.

        if g[0] in keeperList:  # if file in targets was found in the keeperList (items we've marked in config.txt)...
            h = pathlib.Path(f).joinpath(pathHead, f)  # ex. join directory path with stopsign.png for full path to image
            #h = pathlib.PureWindowsPath(h.as_posix())  # changing slashes for later use with windows libraries   
            h = pathlib.Path(str(h).capitalize())
            #  The pathlib library works with Linux-style paths, but we need windows-style paths for scanimage()
            finalFileList.append(h)  # add all of our final filepaths to a list called finalFileList

    # print("final file list: ", finalFileList)  # this list is all targets we will actually track during program loop

    initial_count = count_processes(ulist, process_read())  # store the initial count of running processes
    current_count = []  # variable for the current list of processes to check
    print(initial_count)
    imageRec(0, initial_count, current_count)
    

def imageRec(r, i, c):
    reset_count = r
    global afterID
    global img
    global img_gray
    initial_count = i  # variable for the initial list of processes to check
    current_count = c  # variable for the current list of processes to check
    #  Start of WindowsProcess.py infinite loop segment
    current_count = count_processes(ulist, process_read())  # store the current count of running processes
    if initial_count == current_count:  # check for differences
        print(current_count)  # print current processes
        val = 0
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
    window_capture()
    cv2.destroyAllWindows()
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
    afterID = window.after(1000, imageRec, reset_count, initial_count, current_count)
    #time.sleep(1)  # pause for a moment before checking a new screenshot for resource conservation purposes.

    # can remove if desired or add more delay, doesn't matter but note that currently 1 second per sweep of image

# function that runs whether the user presses the "X" in the top right or if they hit the "Cancel" button
def on_closing():
    print("\nreturning to main window...")
    try:
        os.remove(pathScreenshot)
    except FileNotFoundError:
        print("file not found")
    window.after_cancel(afterID)
    global finalFileList
    finalFileList = []
    runningWindow.withdraw()
    window.deiconify()

def on_quit():
    print("Goodbye.")
    window.destroy()

def validator(x, d):
    # if the 10 char limit has been reached, and not trying to backspace, dont allow
    if len(phoneEntry.get()) == 10:
        if d == '0':
            return True
        return False
    # if they used a number
    elif x.isdigit():
        return True
    # anything else is no-go
    else:
        return False

reg = window.register(validator)

# these couple lines overwrite the control that would normally happen when the user hits the pop-up screen's "X" button
runningWindow.protocol("WM_DELETE_WINDOW", on_closing)
window.protocol("WM_DELETE_WINDOW", on_quit)

# image storage
osasIMG = tk.PhotoImage(file="01.gif")

# messing with Frames
# frame used for logo
imgFrame = tk.Frame(window, width=628, height=207, bg='lightgrey') # w/h is catered towards image provided with x and y + 5 each. currently 623x202
tk.Label(imgFrame, image=osasIMG, bg='white', relief=tk.RAISED, bd=2).pack()
imgFrame.pack(fill=tk.BOTH)

# compact frame used for inputs on left and outputs/status on right
CF = tk.Frame(window)
leftFrame = tk.Frame(CF, bg='lightgrey')
rightFrame = tk.Frame(CF, bg='grey')
outNotifText = tk.Label(rightFrame, text="Program Status:", width=37).pack(fill=tk.BOTH)
inNotifText = tk.Label(leftFrame, text="User Input(s):").pack(fill=tk.BOTH)

# ----------------------------------------------------------------
# ----------------------- LEFT SIDE OF GUI -----------------------
# ----------------------------------------------------------------
# phone entry frame
phoneFrame = tk.Frame(leftFrame, bg='lightgrey')
phoneLabel = tk.Label(phoneFrame, text="Please enter your 10-digit phone number:", bg='lightgrey').pack()
phoneButton = tk.Button(phoneFrame, text="Submit", command=handle_pNum_update_press)
phoneEntry = tk.Entry(phoneFrame, bd=3)
phoneEntry.config(validate="key", validatecommand=(reg, '%S', '%d'))
phoneEntry.pack(side='left', fill=tk.BOTH, expand=tk.TRUE)
phoneButton.pack(side='right')
phoneFrame.pack(expand=tk.TRUE)

# checkboxes frame
checkFrame = tk.Frame(leftFrame, bg='lightgrey')
discCallBox = tk.IntVar()
discCallHalfBox = tk.IntVar()
discTextBox = tk.IntVar()
fireWBox = tk.IntVar()
#custWBox = tk.IntVar()
dotaBox = tk.IntVar()
lolBox = tk.IntVar()
stopBox = tk.IntVar()
dcChk = tk.Checkbutton(checkFrame, text="Discord Call", var=discCallBox, bg='lightgrey')
dchChk = tk.Checkbutton(checkFrame, text="Discord Call (Half Size)", var=discCallHalfBox, bg='lightgrey')
dtChk = tk.Checkbutton(checkFrame, text="Discord Text", var=discTextBox, bg='lightgrey')
fwChk = tk.Checkbutton(checkFrame, text="Firewall Notification", var=fireWBox, bg='lightgrey')
dotaChk = tk.Checkbutton(checkFrame, text="Dota Match Notif.", var=dotaBox, bg='lightgrey')
lolChk = tk.Checkbutton(checkFrame, text="League of Legends Notif", var=lolBox, bg='lightgrey')
stopChk = tk.Checkbutton(checkFrame, text="Stop Sign", var=stopBox, bg='lightgrey')
#custChk = tk.Checkbutton(checkFrame, text="Custom Notification(s)", var=custWBox, bg='lightgrey')
dcChk.pack(anchor='w')
dchChk.pack(anchor = 'w')
dtChk.pack(anchor = 'w')
fwChk.pack(anchor = 'w')
dotaChk.pack(anchor = 'w')
lolChk.pack(anchor = 'w')
stopChk.pack(anchor = 'w')
#custChk.pack(anchor = 'w')
checkFrame.pack(expand=tk.TRUE)

# "Start" and "Close" button
startFrame = tk.Frame(leftFrame, bg='lightgrey')
startButton = tk.Button(startFrame, text="Start", command=handle_button_press)
startButton.pack()
bufFrame3 = tk.Frame(startFrame, height=10, bg='lightgrey').pack()
closeButton = tk.Button(startFrame, text="Close", command=on_quit)
closeButton.pack()
startFrame.pack(expand=tk.TRUE)
# ----------------------------------------------------------------
# ----------------------------------------------------------------


# ----------------------------------------------------------------
# ----------------------- RIGHT SIDE OF GUI ----------------------
# ----------------------------------------------------------------
# status basic output (repeat what is put in phone entry blank)
statusFrame = tk.Frame(rightFrame, bg='grey')
outLabel = tk.Label(statusFrame, text="Value submitted:", bg='grey')
outLabel.pack()
outVal = tk.Label(statusFrame, text=pNum, bg='grey')
outVal.pack()
statusFrame.pack(expand=tk.TRUE)
# ----------------------------------------------------------------
# -----------------------------------------------------------------


# pack the compact frame(s) when done modifying the sides
leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.TRUE)
CF.pack(fill=tk.BOTH, expand=tk.TRUE)

# ----------------------------------------------------------------
# ----------------------- POP-UP WINDOW :) -----------------------
# ----------------------------------------------------------------
# this window will eventually show everything that OSAS will be doing during runtime
# for now, it will just have the "phone number" entered, the checkbox values, and the cancel button
runningFrame = tk.Frame(runningWindow, bg='grey')

# status window listing phone number
runPhoneFrame = tk.Frame(runningFrame, bg='grey')
runLabel = tk.Label(runPhoneFrame, text="Phone Number Chosen:", bg='grey')
runLabel.pack()
runPhoneLabel = tk.Label(runPhoneFrame, text="youwontseethisbuffer", bg='grey')
runPhoneLabel.pack()
runPhoneFrame.pack()

# buffer frame for spacing
bufFrame = tk.Frame(runningFrame, height=20, bg='grey').pack()

# status window listing checkbox choices (currently just integer values)
runCheckboxFrame = tk.Frame(runningFrame, bg='grey')
runCBLabel = tk.Label(runCheckboxFrame, text="Array of detected options selected:", bg='grey')
runCBLabel.pack()
runCB2Label = tk.Label(runCheckboxFrame, text="youwontseethisbuffer", bg='grey')
runCB2Label.pack()
runCheckboxFrame.pack()

# buffer frame for spacing
bufFrame2 = tk.Frame(runningFrame, height=100, bg='grey').pack()

# cancel button
runButtonFrame = tk.Frame(runningFrame, bg='grey')
cancelButton = tk.Button(runButtonFrame, text="Cancel", command=on_closing)
cancelButton.pack()
runButtonFrame.pack(expand=tk.TRUE)

runningFrame.pack(expand=tk.TRUE)
# ----------------------------------------------------------------
# ----------------------------------------------------------------

# start Tkinter
window.mainloop()