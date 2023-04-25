# On-Screen-Alert-System deployment branch

This branch acts as the final version (for now) of the OSAS program runtime.

Once a copy is cloned/downloaded, the user can fill in the redacted data listed in the SID_AUTH_FILE.txt with their own respective data (or contact the creators for the demo data).
Once the file has been filled out, the user can run osasRuntime.py (`python3 osasRuntime.py` or your choice alternative) to launch the program and let it work its magic (you might need to run InstallModules.bat first).


## What is OSAS?

![The On Screen Alert System Logo](./osasLogoLarge.gif)

The On-Screen-Alert-System (or OSAS) is a program made to provide text-based notifications for applications or notifications that would not normally provide remote notifications.
For example, think of firewall/antivirus/install status pop-ups. These never send text messages alerting a user that they popped up. OSAS is capable of recognizing these pop-ups (should the user enable them) and will send the user
a text message based on what phone number they entered into the program earlier on the launch panel.

### Standard steps to use OSAS:

1. Launch OSAS via osasRuntime.py.
2. Enter your phone number in the text entry box and hit submit.
   _ This box only accepts up to 10 numerical digits. Do not worry about the hyphens, it will automatically acount for them.
   _ If you attempt to enter an invalid phone number (a number that is not 10 digits long), or don't enter a number, the program will not let you launch hit the "Start" button.
3. Select all checkbox values you want notifications to be detected for.
4. Click the "Start" button to run the program.

OSAS will now be running and can either be cancelled early by hitting the "Cancel" button or by closing the window that pops up.
Once it detects a notification, it will send a text to the number provided, and put that detected notification on a 5 minute cooldown before it would send another text.