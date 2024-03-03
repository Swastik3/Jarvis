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
import subprocess
from eye_tracker import EyeTracker

class VirtualMouse:
    def __init__(self):
        self.pTime = 0               # Used to calculate frame rate
        self.width = 640             # Width of Camera
        self.height = 480          # Height of Camera
        self.frameR = 100            # Frame Rate
        self.smoothening = 8         # Smoothening Factor
        self.prev_x, self.prev_y = 0, 0   # Previous coordinates
        self.curr_x, self.curr_y = 0, 0   # Current coordinates
        self.prev_x_swipe, self.prev_y_swipe = 0, 0   # Previous coordinates
        self.curr_x_swipe, self.curr_y_swipe = 0, 0   # Current coordinates
        self.flag = 0
        self.slide_counter = 0
        self.lammo = False
        self.dammo = False

        self.speech = STT()

        if os.name == 'nt': self.cap = cv2.VideoCapture(0)
        else: self.cap = cv2.VideoCapture(1)   # Getting video feed from the webcam
        self.cap.set(3, self.width)           # Adjusting size
        self.cap.set(4, self.height)

        self.kb = Controller()
        self.x_threshold = 60 
        #cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

        #tracker = EyeTracker("Image", cap)


        self.detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max

        try:                   # Detecting one hand at max
            self.screen_width = win32api.GetSystemMetrics(0)
            self.screen_height = win32api.GetSystemMetrics(1)     # Getting the screen size
        except:
            self.screen = NSScreen.mainScreen()
            self.frame = self.screen.visibleFrame()
            self.screen_width = self.frame.size.width
            self.screen_height = self.frame.size.height

    def run(self):
        while True:
            success, img = self.cap.read()
            img = self.detector.findHands(img)                       # Finding the hand
            lmlist, bbox = self.detector.findPosition(img)           # Getting position of hand
            #tracker.track_eye_step()

            if len(lmlist)!=0:
                x1, y1 = lmlist[8][1:]
                x2, y2 = lmlist[12][1:]
                x3, y3 = lmlist[16][1:]
                x4, y4 = lmlist[20][1:]
                x5, y5 = lmlist[20][1:]

                fingers = self.detector.fingersUp()      # Checking if fingers are upwards
                cv2.rectangle(img, (self.frameR, self.frameR), (self.width - self.frameR, self.height - self.frameR), (255, 0, 255), 2)   # Creating boundary box
                if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:     # If fore finger is up and middle finger is down
                    cursor_x = np.interp(x3, (self.frameR, self.width-self.frameR), (0,self.screen_width))
                    cursor_y = np.interp(y3, (self.frameR, self.height-self.frameR), (0, self.screen_height))

                    #print(bbox)

                    self.curr_x = (self.prev_x + (cursor_x - self.prev_x)/self.smoothening)
                    self.curr_y = (self.prev_y + (cursor_y - self.prev_y)/self.smoothening)

                    action.move(self.screen_width - self.curr_x, self.curr_y)
                    cv2.circle(img, (x3, y3), 7, (255, 0, 255), cv2.FILLED)
                    self.prev_x, self.prev_y = self.curr_x, self.curr_y
                    length, img, lineInfo = self.detector.findDistance(4, 8, img)

                    if length < 40:     # If both fingers are really close to each other
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        #autopy.action.click()    # Perform Click
                        action.click()
                        #print("click")
                        time.sleep(0.35)
                        if length < 25:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            #autopy.action.click()    # Perform Click
                            action.click()
                            #print("click")
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
                    length, img, lineInfo = self.detector.findDistance(8, 16, img)

                    if length < 40:
                        pyautogui.scroll(80)

                    if length > 100:
                        pyautogui.scroll(-80)

                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    length, img, lineInfo = self.detector.findDistance(8, 12, img)

                    if length < 40 and flag != 1:
                        #print("pressed")
                        action.press(button = "left")
                        flag = 1
                    elif flag == 1 and length > 40:
                        #print("released")
                        action.release(button = "left")
                        flag = 0

                    cursor_x = np.interp(x3, (self.frameR,self.width-self.frameR), (0,self.screen_width))
                    cursor_y = np.interp(y3, (self.frameR, self.height-self.frameR), (0, self.screen_height))

                    curr_x = prev_x + (cursor_x - prev_x)/self.smoothening
                    curr_y = prev_y + (cursor_y - prev_y) / self.smoothening

                    action.move(self.screen_width - curr_x,curr_y)
                    cv2.circle(img, (x3, y3), 7, (255, 0, 255), cv2.FILLED)
                    prev_x, prev_y = curr_x, curr_y

                elif fingers[2]== 1 and fingers[0]==1 and fingers[4]==1 and fingers[3]==0 and fingers[1]==0 and lammo==False:
                    #print("snappp")
                    lammo=True    
                    webbrowser.open("https://www.youtube.com/watch?v=hw2eOKy5w9g&pp=ygUQbW91bnRhaW4gZGV3IGRhcg%3D%3D", new=2)

                elif fingers[0]== 1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0 and dammo==False:
                    #print("ppp") 
                    dammo=True
                    #subprocess.run(r'"Tera Term.lnk"')
                    #p = subprocess.Popen([r"C:\Users\sange\OneDrive\Documents\teraterm\ttermpro.exe", '/SHOW'])
                
                    self.arduino_control()
                    time.sleep(0.5)
                    #p.terminate()

                elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    length, img, lineInfo = self.detector.findDistance(16, 20, img)
                    if length > 60:
                        exit()

                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    self.speech.record_audio(duration=4)
                    text = self.speech.transcribe()
                    string = " ".join(text)
                    for char in string:
                        self.kb.press(char)
                        self.kb.release(char)
                    time.sleep(0.2)

                elif all(lmlist[i][2] > 0 for i in [8, 12, 16, 20]):
                    cursor_x = np.interp(x3, (self.frameR, self.width - self.frameR), (0, self.screen_width))
                    cursor_y = np.interp(y3, (self.frameR, self.height - self.frameR), (0, self.screen_height))

                    self.curr_x = self.prev_x + (cursor_x - self.prev_x) / self.smoothening
                    self.curr_y = self.prev_y + (cursor_y - self.prev_y) / self.smoothening

                    # Check if sliding left and movement surpasses the threshold
                    if curr_x < prev_x and abs(curr_x - prev_x) > self.x_threshold:
                        slide_counter += 1
                        if slide_counter > 6:
                            #print("slide left")
                            self.kb.press(Key.left)  # Simulate pressing the left arrow key
                            self.kb.release(Key.left) 
                            time.sleep(0.7) # Simulate releasing the left arrow key
                    elif curr_x > prev_x and abs(curr_x - prev_x) > self.x_threshold:
                        slide_counter += 1
                        if slide_counter > 6:
                            #print("slide right")
                            self.kb.press(Key.right)  # Simulate pressing the left arrow key
                            self.kb.release(Key.right)
                            time.sleep(0.7) # Simulate releasing the left arrow key  
                    prev_x, prev_y = curr_x, curr_y

            self.cTime = time.time()
            fps = 1/(self.cTime - self.pTime)
            self.pTime = self.cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)

    def arduino_control(self):
        while True:
            success, img = self.cap.read()
            img = self.detector.findHands(img)                       # Finding the hand
            lmlist, bbox = self.detector.findPosition(img)           # Getting position of hand

            if len(lmlist)!=0:
                x1, y1 = lmlist[8][1:]
                x2, y2 = lmlist[12][1:]
                x3, y3 = lmlist[16][1:]
                x4, y4 = lmlist[20][1:]
                x5, y5 = lmlist[20][1:]

                fingers = self.detector.fingersUp()      # Checking if fingers are upwards
                cv2.rectangle(img, (self.frameR, self.frameR), (self.width - self.frameR, self.height - self.frameR), (255, 0, 255), 2)   # Creating boundary box

                if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:     # If fore finger is up and middle finger is down
                    cursor_x = np.interp(x3, (self.frameR,self.width-self.frameR), (0,self.screen_width))
                    cursor_y = np.interp(y3, (self.frameR, self.height-self.frameR), (0, self.screen_height))

                    #print(bbox)

                    curr_x = (prev_x + (cursor_x - prev_x)/self.smoothening)
                    curr_y = (prev_y + (cursor_y - prev_y) / self.smoothening)

                    action.move(self.screen_width - curr_x,curr_y)
                    cv2.circle(img, (x3, y3), 7, (255, 0, 255), cv2.FILLED)
                    prev_x, prev_y = curr_x, curr_y
                    length, img, lineInfo = self.detector.findDistance(4, 8, img)

                    if length < 40:     # If both fingers are really close to each other
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        #autopy.action.click()    # Perform Click
                        action.click()
                        #print("click")
                        time.sleep(0.35)
                        if length < 25:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            #autopy.action.click()    # Perform Click
                            action.click()
                            #print("click")
                        else:
                            time.sleep(0.25)

                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:     # If fore finger & middle finger both are up
                    length, img, lineInfo = self.detector.findDistance(8, 12, img)

                    if length < 40:
                        #print("pressing z")
                        self.kb.press("z")
                    elif length > 80:
                        #print("pressing x")
                        self.kb.press("x")

                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:     # If fore finger & middle finger both are up
                    length, img, lineInfo = self.detector.findDistance(8, 16, img)

                    if length < 50:
                        #print("pressing a")
                        self.kb.press("a")
                    elif length > 100:
                        #print("pressing d")
                        self.kb.press("d")

                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:     # If fore finger & middle finger both are up
                    length, img, lineInfo = self.detector.findDistance(8, 20, img)

                    if length < 80:
                        #print("pressing w")
                        self.kb.press("w")
                    elif length > 120:
                        #print("pressing s")
                        self.kb.press("s")

                elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:     # If fore finger & middle finger both are up
                    self.kb.press("1")
                
                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:     # If fore finger & middle finger both are up
                    self.kb.press("2")

                elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:     # If fore finger & middle finger both are up
                    self.kb.press("3")

                elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    length, img, lineInfo = self.detector.findDistance(16, 20, img)
                    if length > 60:
                        #print("exiting")
                        dammo = False
                        return

            self.cTime = time.time()
            fps = 1/(self.cTime-self.pTime)
            self.pTime = self.cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)


def main():
    vm = VirtualMouse()
    vm.run()
    
if __name__ == "__main__":
    main()