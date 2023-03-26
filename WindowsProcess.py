from ast import If
import os


#importing libraries 
import pyautogui
import cv2  #this is installed with the following command in command prompt: "pip install opencv-contrib-python"
import numpy 
from time import process_time_ns
import msvcrt
import pathlib
import time



#creating variables for lists of processes
ulist = []                                                 #create variable for user list of values to check
initial_count = []                                         #variable for the initial list of processes to check
current_count = []                                         #variable for the current list of processes to check
process_time = 5                                           #variable to set the time between process checks in seconds


#read config file for processes to watch
with open('config.txt', 'r') as f:                         #open config file
    for line in f:                                         #iterate through file
        if line.startswith('*'):                           #check for process character (*)
            ulist.append(line.lstrip('*').strip())         #format output and add to ulist


#####---------------------------------------------------------------------------START_OF_FUNCTIONS---------------------------------------------------------------------------#####

#Function to create list of processes running on host machine
def process_read():
    process_count = {}                                                          #create variable for processes to be counted
    process_current = os.popen('wmic process get description').read()           # read list of current processes   
    process_list = process_current.strip().split('\n')[1:]                      # remove header line and split by newline
    process_set = set(process_list)                                             # convert to set to remove duplicates
    # loop to find occurrences of each process
    for process in process_set:                                                 # iterate through 'process set' array
        count = process_list.count(process)                                     # count the number of processes
        process_count[process] = count                                          # create dictionary of processes

    process_output = [f"{process} ({count})".strip() for process, count in process_count.items()]   # put the contents of the previous loop together
    return process_output                                                       #return the list of processes dictionary


#Compare the processes in the config file to the processes recorded running on the machine
def count_processes(ulist, process_output):
    entry_counts = {}                                          #create variable for number of entries
    for process in ulist:
        count = 0
        for output in process_output:
            if process.lower() in output.lower():
                count += int(output.split("(")[1].split(")")[0])
        entry_counts[process] = count
    return entry_counts





#####----------------------------------------------------------------------------END_OF_FUNCTIONS----------------------------------------------------------------------------#####



initial_count = count_processes(ulist, process_read())                      #store the initial count of running processes
print(initial_count)
reset_count=0
while True:
    current_count = count_processes(ulist, process_read())                  #store the current count of running processes
    if (initial_count == current_count):                                    #check for differences
        print(current_count)                                                #print current processes
    elif (reset_count==0):                                                  #check if reset if complete
        print(current_count)                                                #print current processes
        print('output to API')                                              #"output to API"
        reset_count = 5                                                     #Set Reset Counter to x * process_time
    else :
        print (current_count)                                               #print current ptocesses
        reset_count = reset_count -1                                        #itterate counter down by 1
    time.sleep(process_time)                                                #pause for process_time

