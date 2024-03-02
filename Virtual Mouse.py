import cv2
import numpy as np
import time
import HandTracking as ht
import os
import sys
if os.name == 'nt': import win32api
else: from AppKit import NSScreen
import time
import action
#import autopy   # Install using "pip install autopy"\
from pynput.keyboard import Key, Controller
import pyautogui
import webbrowser
from STT import STT

### Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480          # Height of Camera
frameR = 100            # Frame Rate
smoothening = 8         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates
prev_x_swipe, prev_y_swipe = 0, 0   # Previous coordinates
curr_x_swipe, curr_y_swipe = 0, 0   # Current coordinates
flag = 0
slide_counter = 0
lammo = False

speech = STT()

if os.name == 'nt': cap = cv2.VideoCapture(0)
else: cap = cv2.VideoCapture(1)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)

kb = Controller()
x_threshold = 60 


detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max


try:                   # Detecting one hand at max
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)     # Getting the screen size
except:
    screen = NSScreen.mainScreen()
    frame = screen.visibleFrame()
    screen_width = frame.size.width
    screen_height = frame.size.height
   # Getting the screen size
while True:
    success, img = cap.read()
    img = detector.findHands(img)                       # Finding the hand
    lmlist, bbox = detector.findPosition(img)           # Getting position of hand

    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        x3, y3 = lmlist[16][1:]
        x4, y4 = lmlist[20][1:]
        x5, y5 = lmlist[20][1:]

        fingers = detector.fingersUp()      # Checking if fingers are upwards
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)   # Creating boundary box
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:     # If fore finger is up and middle finger is down
            cursor_x = np.interp(x3, (frameR,width-frameR), (0,screen_width))
            cursor_y = np.interp(y3, (frameR, height-frameR), (0, screen_height))

            print(bbox)

            curr_x = (prev_x + (cursor_x - prev_x)/smoothening)
            curr_y = (prev_y + (cursor_y - prev_y) / smoothening)

            action.move(screen_width - curr_x,curr_y)
            cv2.circle(img, (x3, y3), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y
            length, img, lineInfo = detector.findDistance(4, 8, img)

            if length < 40:     # If both fingers are really close to each other
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                #autopy.action.click()    # Perform Click
                action.click()
                print("click")
                time.sleep(0.35)
                if length < 25:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    #autopy.action.click()    # Perform Click
                    action.click()
                    print("click")
                else:
                    time.sleep(0.25)

        # elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:     # If fore finger & middle finger both are up
        #     length, img, lineInfo = detector.findDistance(4, 8, img)

        #     if length < 40:     # If both fingers are really close to each other
        #         cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
        #         #autopy.action.click()    # Perform Click
        #         action.click()
        #         print("click")
        #         time.sleep(0.5)

        # elif fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        #     kb.press(Key.left)
        #     time.sleep(0.5)

        # elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        #     kb.press(Key.right)
        #     time.sleep(0.5)

        elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
            length, img, lineInfo = detector.findDistance(8, 16, img)

            if length < 40:
                pyautogui.scroll(80)

            if length > 100:
                pyautogui.scroll(-80)

        elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40 and flag != 1:
                print("pressed")
                action.press(button = "left")
                flag = 1
            elif flag == 1 and length > 40:
                print("released")
                action.release(button = "left")
                flag = 0

            cursor_x = np.interp(x3, (frameR,width-frameR), (0,screen_width))
            cursor_y = np.interp(y3, (frameR, height-frameR), (0, screen_height))

            curr_x = prev_x + (cursor_x - prev_x)/smoothening
            curr_y = prev_y + (cursor_y - prev_y) / smoothening

            action.move(screen_width - curr_x,curr_y)
            cv2.circle(img, (x3, y3), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        elif fingers[2]== 1 and fingers[0]==1 and fingers[4]==1 and fingers[3]==0 and fingers[1]==0 and lammo==False:
            print("snappp")
            lammo=True    
            webbrowser.open("https://www.youtube.com/watch?v=hw2eOKy5w9g&pp=ygUQbW91bnRhaW4gZGV3IGRhcg%3D%3D", new=2)
        elif fingers[0]== 0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:
            print("ppp") 
            os.system(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Tera Term\Tera Term.lnk")

        elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            length, img, lineInfo = detector.findDistance(16, 20, img)
            if length > 60:
                exit()

        elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            speech.record_audio(duration=4)
            text = speech.transcribe()
            string = " ".join(text)
            for char in string:
                kb.press(char)
                kb.release(char)
            time.sleep(0.2)

        elif all(lmlist[i][2] > 0 for i in [8, 12, 16, 20]):
            cursor_x = np.interp(x3, (frameR, width - frameR), (0, screen_width))
            cursor_y = np.interp(y3, (frameR, height - frameR), (0, screen_height))

            curr_x = prev_x + (cursor_x - prev_x) / smoothening
            curr_y = prev_y + (cursor_y - prev_y) / smoothening

            # Check if sliding left and movement surpasses the threshold
            if curr_x < prev_x and abs(curr_x - prev_x) > x_threshold:
                slide_counter += 1
                if slide_counter > 6:
                    print("slide left")
                    kb.press(Key.left)  # Simulate pressing the left arrow key
                    kb.release(Key.left) 
                    time.sleep(0.7) # Simulate releasing the left arrow key
            elif curr_x > prev_x and abs(curr_x - prev_x) > x_threshold:
                slide_counter += 1
                if slide_counter > 6:
                    print("slide right")
                    kb.press(Key.right)  # Simulate pressing the left arrow key
                    kb.release(Key.right)
                    time.sleep(0.7) # Simulate releasing the left arrow key  
            prev_x, prev_y = curr_x, curr_y

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
