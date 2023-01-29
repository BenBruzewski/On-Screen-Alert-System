# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:11:10 2023

@author: Ben
filename: detectImage.py
description: Checking to see if we can spot an image when it is part of a pic
date: 1/25/23
"""

import pyautogui # take screenshots 
import cv2 # display images
import numpy as np # 
from time import process_time_ns # needed for time estimate

print('\n new run ...')
t1_start = process_time_ns() # recording elapsed time so we know what to expect

# for i in range (0,10): # Can enable this and tab next 2 lines to see 1 second
screenshot1 = pyautogui.screenshot()
screenshot1.save(r'C:\Users\Ben\Python_Projects\screenshot1.png')

img = cv2.imread('C:/Users/Ben/Python_Projects/screenshot1.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow("Screenshot", img)
 
target_img = cv2.imread('C:/Users/Ben/Python_Projects/StopSign.png',0) 

w, h = target_img.shape[::-1]

res = cv2.matchTemplate(img_gray,target_img,cv2.TM_CCOEFF_NORMED)

threshold = 0.8

loc = np.where(res >= threshold)

counter = 0

for pt in zip(*loc[::-1]):
    cv2.rectangle(img,pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    confidence = res[pt[1]][pt[0]]
    print('conf = ', confidence)
    cv2.imshow(' ',img)
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


cv2.waitKey(0)

t1_stop = process_time_ns()

print("Elapsed time during the whole program in nanoseconds:", t1_stop-t1_start)
print("Elapsed time during the whole program in seconds:", (t1_stop-t1_start) / 1000000000)

