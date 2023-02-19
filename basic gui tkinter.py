import tkinter as tk

window = tk.Tk()
window.title("On Screen Alert System")
window.configure(background="white") # this background can accept hexRGB values (eg. #6FAFE7)
window.minsize(900, 600)
window.maxsize(900, 600)
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("900x600+%d+%d" % ((w/2)-450, (h/2)-300)) # starting dims and x/y coords
pNum = "why"

# handler to accept user's update from phone number text box
def handle_pNum_update_press():
    pNum = phoneEntry.get()
    outVal.configure(text=pNum)

# currently debugs output into terminal
def handle_button_press():
    print("button pressed. pNum val =", pNum)
    print("checkboxes values are noted as: %d, %d, %d, %d" % (discCallBox.get(), discCallHalfBox.get(), discTextBox.get(), fireWBox.get()))

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


# ----------------------- LEFT SIDE OF GUI -----------------------
# phone entry frame
phoneFrame = tk.Frame(leftFrame)
phoneButton = tk.Button(phoneFrame, text="Submit", command=handle_pNum_update_press).pack(side='right')
phoneEntry = tk.Entry(phoneFrame, bd=3)
phoneEntry.pack(side='left')
phoneFrame.pack(expand=tk.TRUE)

# checkboxes frame
checkFrame = tk.Frame(leftFrame, bg='lightgrey')
discCallBox = tk.IntVar()
discCallHalfBox = tk.IntVar()
discTextBox = tk.IntVar()
fireWBox = tk.IntVar()
dcChk = tk.Checkbutton(checkFrame, text="Discord Call", var=discCallBox, bg='lightgrey')
dchChk = tk.Checkbutton(checkFrame, text="Discord Call (Half Size)", var=discCallHalfBox, bg='lightgrey')
dtChk = tk.Checkbutton(checkFrame, text="Discord Text", var=discTextBox, bg='lightgrey')
fwChk = tk.Checkbutton(checkFrame, text="Firewall Notification", var=fireWBox, bg='lightgrey')
dcChk.pack(anchor='w')
dchChk.pack(anchor = 'w')
dtChk.pack(anchor = 'w')
fwChk.pack(anchor = 'w')
checkFrame.pack(expand=tk.TRUE)

# "Start" button
startFrame = tk.Frame(leftFrame)
startButton = tk.Button(startFrame, text="Start", command=handle_button_press).pack()
startFrame.pack(expand=tk.TRUE)
# ----------------------------------------------------------------


# ----------------------- RIGHT SIDE OF GUI -----------------------
# status basic output (repeat what is put in phone entry blank)
statusFrame = tk.Frame(rightFrame, bg='grey')
outLabel = tk.Label(statusFrame, text="Value submitted:", bg='grey')
outLabel.pack()
outVal = tk.Label(statusFrame, text=pNum, bg='grey')
outVal.pack()
statusFrame.pack(expand=tk.TRUE)
# -----------------------------------------------------------------


# pack the compact frame(s) when done modifying the sides
leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.TRUE)
CF.pack(fill=tk.BOTH, expand=tk.TRUE)

# launch the actual window
window.mainloop()