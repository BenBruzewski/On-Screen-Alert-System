import tkinter as tk
from configparser import ConfigParser

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
# create the configparsing object
confObj = ConfigParser()

# handler to accept user's update from phone number text box
def handle_pNum_update_press():
    pNum = phoneEntry.get()
    outVal.configure(text=pNum)

# currently debugs output into terminal
def handle_button_press():
    runPhoneLabel.configure(text=outVal.cget("text"))
    runCB2Label.configure(text="%d, %d, %d, %d, %d" % (discCallBox.get(), discCallHalfBox.get(), discTextBox.get(), fireWBox.get(), custWBox.get()))
    # modify the config file
    confObj.read("config.ini")
    trackedImg = confObj["TRACKEDIMAGES"]
    trackedImg["discord_call_full"] = "%d" % discCallBox.get()
    trackedImg["discord_call_half"] = "%d" % discCallHalfBox.get()
    trackedImg["discord_text"] = "%d" % discTextBox.get()
    trackedImg["windows_firewall"] = "%d" % fireWBox.get()
    trackedImg["custom_notif"] = "%d" % custWBox.get()
    with open('config.ini', 'w') as conf:
        confObj.write(conf)
    window.withdraw()
    runningWindow.deiconify()

# function that runs whether the user presses the "X" in the top right or if they hit the "Cancel" button
def on_closing():
    print("\nreturning to main window...")
    runningWindow.withdraw()
    window.deiconify()

def on_quit():
    print("Goodbye.")
    window.destroy()

def validator(x):
    # if they used a number
    if x.isdigit():
        return True
    # if they backspaced
    elif x == "":
        return True
    # anything else is no-go
    else:
        return False

reg = window.register(validator)

# this single line overwrites the control that would normally happen when the user hits the pop-up screen's "X" button
runningWindow.protocol("WM_DELETE_WINDOW", on_closing)

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
outNotifText = tk.Label(rightFrame, text="Program Status:").pack(fill=tk.BOTH)
inNotifText = tk.Label(leftFrame, text="User Input(s):").pack(fill=tk.BOTH)

# ----------------------------------------------------------------
# ----------------------- LEFT SIDE OF GUI -----------------------
# ----------------------------------------------------------------
# phone entry frame
phoneFrame = tk.Frame(leftFrame)
phoneButton = tk.Button(phoneFrame, text="Submit", command=handle_pNum_update_press).pack(side='right')
phoneEntry = tk.Entry(phoneFrame, bd=3)
phoneEntry.config(validate="key", validatecommand=(reg, '%P'))
phoneEntry.pack(side='left')
phoneFrame.pack(expand=tk.TRUE)

# checkboxes frame
checkFrame = tk.Frame(leftFrame, bg='lightgrey')
discCallBox = tk.IntVar()
discCallHalfBox = tk.IntVar()
discTextBox = tk.IntVar()
fireWBox = tk.IntVar()
custWBox = tk.IntVar()
dcChk = tk.Checkbutton(checkFrame, text="Discord Call", var=discCallBox, bg='lightgrey')
dchChk = tk.Checkbutton(checkFrame, text="Discord Call (Half Size)", var=discCallHalfBox, bg='lightgrey')
dtChk = tk.Checkbutton(checkFrame, text="Discord Text", var=discTextBox, bg='lightgrey')
fwChk = tk.Checkbutton(checkFrame, text="Firewall Notification", var=fireWBox, bg='lightgrey')
custChk = tk.Checkbutton(checkFrame, text="Custom Notification(s)", var=custWBox, bg='lightgrey')
dcChk.pack(anchor='w')
dchChk.pack(anchor = 'w')
dtChk.pack(anchor = 'w')
fwChk.pack(anchor = 'w')
custChk.pack(anchor = 'w')
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