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
from RealtimeSTT import AudioToTextRecorder
import os
import playsound as playsound

from threading import Thread
import pydub


### Variables Declaration

class VirtualMouse:
    def __init__(self):
        self.pTime = 0               # Used to calculate frame rate
        self.width = 640             # Width of Camera
        self.height = 480         # Height of Camera
        self.smoothening = 6         # self.smoothening Factor
        self.prev_x, self.prev_y = 0, 0   # Previous coordinates
        self.curr_x, self.curr_y = 0, 0   # Current coordinates
        self.flag = 0
        self.slide_counter_right = 0
        self.slide_counter_left = 0
        self.lammo = False
        self.dammo = False
        self.gammo=False
        self.speech = STT()

        if os.name == 'nt': self.cap = cv2.VideoCapture(0)
        else: self.cap = cv2.Video.capture(1)   # Getting video feed from the webcam
        self.cap.set(3, self.width)           # Adjusting size
        self.cap.set(4, self.height)

        self.kb = Controller()
        self.x_threshold = 60 
        #cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

        #tracker = EyeTracker("Image", self.cap)


        self.detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max


        try:                   # Detecting one hand at max
            self.screen_width = win32api.GetSystemMetrics(0)
            self.screen_height = win32api.GetSystemMetrics(1)     # Getting the screen size
        except:
            screen = NSScreen.mainScreen()
            frame = screen.visibleFrame()
            self.screen_width = frame.size.width
            self.screen_height = frame.size.height

        
        self.click_timer = 0
        self.right_click_timer = 0
        self.record_timer = 0
        self.slide_timer = 0
        self.exit_timer = 0
        self.can_double_click = True
        
# Getting the screen size

    def perform_click(self):
        print("clicking")
        Thread(target=action.click).start()
        self.click_timer = 20
    
    def perform_right_click(self):
        print("right clicking")
        Thread(target=action.click, args=("right",)).start()
        self.right_click_timer = 20
    
    def perform_record(self):
        print("recording")
        def record_inner(speech,kb):
            speech.record_audio(duration=2)
            text = speech.transcribe()
            string = " ".join(text)
            for char in string:
                kb.press(char)
                kb.release(char)
        Thread(target=record_inner, args=(self.speech,self.kb)).start()
        self.record_timer = 200
    
    def perform_slide_right(self):
        print("sliding right")
        def slide_right():
            self.kb.press(Key.right)  # Simulate pressing the right arrow key
            self.kb.release(Key.right)
        Thread(target=slide_right).start()
        self.slide_timer = 30
    
    def perform_slide_left(self):
        print("sliding left")
        def slide_left():
            self.kb.press(Key.left)  # Simulate pressing the left arrow key
            self.kb.release(Key.left)
        Thread(target=slide_left).start()
        self.slide_timer = 30
    
    def arduino_control(self):
        ricko = False
        shitto = False
        frameR = 100
        while True:
            success, img = self.cap.read()
            img = self.detector.findHands(img)                       # Finding the hand
            lmlist, bbox = self.detector.findPosition(img)           # Getting position of hand

            if len(lmlist)!=0:
                #x1, y1 = lmlist[8][1:]
                #x2, y2 = lmlist[12][1:]
                x3, y3 = lmlist[16][1:]
                #x4, y4 = lmlist[20][1:]
                #x5, y5 = lmlist[20][1:]

                fingers = self.detector.fingersUp()      # Checking if fingers are upwards
                cv2.rectangle(img, (frameR, frameR), (self.width - frameR, self.height - frameR), (255, 0, 255), 2)   # Creating boundary box

                if fingers == [1,1,0,0,0]:     # If fore finger is up and middle finger is down
                    cursor_x = np.interp(x3, (frameR,self.width-frameR), (0,self.screen_width))
                    cursor_y = np.interp(y3, (frameR, self.height-frameR), (0, self.screen_height))

                    #print(bbox)

                    self.curr_x = (self.prev_x + (cursor_x - self.prev_x)/self.smoothening)
                    self.curr_y = (self.prev_y + (cursor_y - self.prev_y) / self.smoothening)

                    action.move(self.screen_width - self.curr_x,self.curr_y)
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

                elif fingers == [0,1,1,0,0]:     # If fore finger & middle finger both are up
                    length, img, lineInfo = self.detector.findDistance(8, 12, img)

                    if length < 40:
                        #print("pressing z")
                        self.kb.press("z")
                    elif length > 80:
                        #print("pressing x")
                        self.kb.press("x")

                elif fingers == [0,1,1,1,0]:     # If fore finger & middle finger both are up
                    length, img, lineInfo = self.detector.findDistance(8, 16, img)

                    if length < 50:
                        #print("pressing a")
                        self.kb.press("a")
                    elif length > 100:
                        #print("pressing d")
                        self.kb.press("d")

                elif fingers == [0,1,1,1,1]:     # If fore finger & middle finger both are up
                    length, img, lineInfo = self.detector.findDistance(8, 20, img)

                    if length < 80:
                        #print("pressing w")
                        self.kb.press("w")
                    elif length > 120:
                        #print("pressing s")
                        self.kb.press("s")

                elif fingers == [1,1,0,0,1]:     # If fore finger & middle finger both are up
                    self.kb.press("1")
                
                elif fingers == [0,1,0,0,1]:     # If fore finger & middle finger both are up
                    self.kb.press("2")

                elif fingers == [1,1,1,0,0]:     # If fore finger & middle finger both are up
                    self.kb.press("3")

                elif fingers == [1,0,1,0,1] and [ricko==False]:     # If fore finger & middle finger both are up
                    #print("snappp")
                    self.kb.press("4")
                    ricko == True
                    time.sleep(0.5)
                
                elif fingers == [0,0,1,1,1] and shitto == False:
                    self.kb.press("h")
                    shitto = True
                    time.sleep(0.5)

                elif fingers == [0,0,0,0,1]:
                    length, img, lineInfo = self.detector.findDistance(16, 20, img)
                    if length > 60:
                        if self.exit_timer == 0:
                            print("exiting")
                            self.dammo = False
                            self.exit_timer = 60
                            return

            cTime = time.time()
            fps = 1/(cTime-self.pTime)
            self.pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)

    
    def guitar(self):
        stack_sound = pydub.AudioSegment.silent(duration=0)
        
        
        print("entering guitar mode")
        timer_duration = 15
        guitar_sound_timer = 0
        frameR = 100
        while True:
            success, img = self.cap.read()
            img = self.detector.findHands(img)                       # Finding the hand
            lmlist, bbox = self.detector.findPosition(img)           # Getting position of hand
            

            if len(lmlist)!=0:

                fingers = self.detector.fingersUp()      # Checking if fingers are upwards
                cv2.rectangle(img, (frameR, frameR), (self.width - frameR, self.height - frameR), (255, 0, 255), 2) 

                if fingers == [0,1,1,0,0]:
                    if guitar_sound_timer == 0:
                        print("E")
                        Thread(target=playsound.playsound, args=(r'sounds\e-64kb_0aT5gGDo.mp3',)).start()
                        stack_sound += pydub.AudioSegment.from_file(r'sounds\e-64kb_0aT5gGDo.mp3')
                        guitar_sound_timer = timer_duration

                elif fingers == [1,1,1,1,0]:
                    if guitar_sound_timer == 0:
                        print("C")
                        Thread(target=playsound.playsound, args=(r'sounds\c-64kb_tGx61ISi.mp3',)).start()
                        stack_sound += pydub.AudioSegment.from_file(r'sounds\c-64kb_tGx61ISi.mp3')
                        guitar_sound_timer = timer_duration
                    

                elif fingers == [1,1,0,0,1]:
                    if guitar_sound_timer == 0:
                        print("G")
                        Thread(target=playsound.playsound, args=(r'sounds\g-64kb_kaTudOcK.mp3',)).start()
                        stack_sound += pydub.AudioSegment.from_file(r'sounds\g-64kb_kaTudOcK.mp3')
                        guitar_sound_timer = timer_duration
                    

                elif fingers == [1,1,1,0,0]:
                    if guitar_sound_timer == 0:
                        print("D")
                        Thread(target=playsound.playsound, args=(r'sounds\d-64kb_4ymAcwfO.mp3',)).start()
                        stack_sound += pydub.AudioSegment.from_file(r'sounds\d-64kb_4ymAcwfO.mp3')
                        guitar_sound_timer = timer_duration
                    

                elif fingers == [0,0,0,0,1]:
                    length, img, lineInfo = self.detector.findDistance(16, 20, img)
                    stack_sound.export(r"tmp\guitar_stack.mp3", format="mp3")
                    #playsound.playsound(r"tmp\guitar_stack.mp3")
                    if length > 60:
                        print("exiting")
                        self.exit_timer = 60
                        return


            cTime = time.time()
            fps = 1/(cTime-self.pTime)
            self.pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            guitar_sound_timer = max(0, guitar_sound_timer - 1)

    def run(self):
        frameR = 100
        while True:
            success, img = self.cap.read()
            img = self.detector.findHands(img)                       # Finding the hand
            lmlist, bbox = self.detector.findPosition(img)           # Getting position of hand
            #tracker.track_eye_step()

            if len(lmlist)!=0:
                #x1, y1 = lmlist[8][1:]
                #x2, y2 = lmlist[12][1:]
                x3, y3 = lmlist[16][1:]
                #x4, y4 = lmlist[20][1:]
                #x5, y5 = lmlist[20][1:]

                fingers = self.detector.fingersUp()      # Checking if fingers are upwards
                cv2.rectangle(img, (frameR, frameR), (self.width - frameR, self.height - frameR), (255, 0, 255), 2)   # Creating boundary box
                
                if fingers == [1,1,0,0,0]:
                    cursor_x = np.interp(x3, (frameR,self.width-frameR), (0,self.screen_width))
                    cursor_y = np.interp(y3, (frameR, self.height-frameR), (0, self.screen_height))

                    #print(bbox)

                    self.curr_x = (self.prev_x + (cursor_x - self.prev_x)/self.smoothening)
                    self.curr_y = (self.prev_y + (cursor_y - self.prev_y) / self.smoothening)

                    action.move(self.screen_width - self.curr_x,self.curr_y)
                    cv2.circle(img, (x3, y3), 7, (255, 0, 255), cv2.FILLED)
                    self.prev_x, self.prev_y = self.curr_x, self.curr_y
                    length, img, lineInfo = self.detector.findDistance(4, 8, img)

                    if self.curr_x > 2000 or self.curr_y > 1400 or self.curr_x < 200 or self.curr_y < 100:
                        if length < 70:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            if self.click_timer == 0:
                                self.can_double_click = True
                                self.perform_click()
                            
                            #TODO: do we need this?
                            if length < 40:
                                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                                if self.can_double_click and 12 < self.click_timer < 18:
                                    self.can_double_click = False
                                    print("shady click")
                                    self.perform_click()
                            else:
                                #time.sleep(0.25)
                                pass

                    elif length < 40:     # If both fingers are really close to each other
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                           # Perform Click
                        if self.click_timer == 0:
                            self.can_double_click = True
                            self.perform_click()
                        
                        if length < 20:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            #autopy.action.click()    # Perform Click
                            if 15 < self.click_timer < 18 and self.can_double_click:
                                print("double click")
                                self.can_double_click = False
                                self.perform_click()

                elif fingers == [1,1,1,0,0]:
                        cursor_x = np.interp(x3, (frameR,self.width-frameR), (0,self.screen_width))
                        cursor_y = np.interp(y3, (frameR, self.height-frameR), (0, self.screen_height))

                        #print(bbox)

                        self.curr_x = (self.prev_x + (cursor_x - self.prev_x)/self.smoothening)
                        self.curr_y = (self.prev_y + (cursor_y - self.prev_y) / self.smoothening)

                        action.move(self.screen_width - self.curr_x,self.curr_y)
                        cv2.circle(img, (x3, y3), 7, (255, 0, 255), cv2.FILLED)
                        self.prev_x, self.prev_y = self.curr_x, self.curr_y
                        length1, img, lineInfo = self.detector.findDistance(4, 8, img)
                        length2, img, lineInfo = self.detector.findDistance(4, 12, img)

                        if length1 < 40 and length2 < 40:     # If both fingers are really close to each other
                            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            #autopy.action.click()    # Perform Click
                            if self.right_click_timer == 0:
                                self.perform_right_click()

                elif fingers == [0,1,1,1,0]:
                    length, img, lineInfo = self.detector.findDistance(8, 16, img)
                    #print(length)

                    if length < 40:
                        pyautogui.scroll(80)

                    if length > 100:
                        pyautogui.scroll(-80)

                elif fingers == [0,1,1,0,0]:
                    length, img, lineInfo = self.detector.findDistance(8, 12, img)

                    if length < 40 and self.flag != 1:
                        #print("pressed")
                        action.press(button = "left")
                        self.flag = 1
                    elif self.flag == 1 and length > 40:
                        #print("released")
                        action.release(button = "left")
                        self.flag = 0

                    cursor_x = np.interp(x3, (frameR,self.width-frameR), (0,self.screen_width))
                    cursor_y = np.interp(y3, (frameR, self.height-frameR), (0, self.screen_height))

                    self.curr_x = self.prev_x + (cursor_x - self.prev_x)/self.smoothening
                    self.curr_y = self.prev_y + (cursor_y - self.prev_y) / self.smoothening

                    action.move(self.screen_width - self.curr_x,self.curr_y)
                    cv2.circle(img, (x3, y3), 7, (255, 0, 255), cv2.FILLED)
                    self.prev_x, self.prev_y = self.curr_x, self.curr_y

                elif fingers == [1,0,1,0,1] and [self.lammo==False]:
                    #print("snappp")
                    self.lammo=True    
                    webbrowser.open("https://www.youtube.com/watch?v=hw2eOKy5w9g&pp=ygUQbW91bnRhaW4gZGV3IGRhcg%3D%3D", new=2)

                elif fingers == [1,1,1,1,0] and self.dammo==False:
                    #print("ppp") 
                    self.dammo=True
                    #subprocess.run(r'"Tera Term.lnk"')
                    #p = subprocess.Popen([r"C:\Users\sange\OneDrive\Documents\teraterm\ttermpro.exe", '/SHOW'])
                
                    self.arduino_control()
                    time.sleep(0.5)
                    #p.terminate()
                elif fingers == [0,0,1,1,1] and self.gammo==False:
                    self.gammo=True
                    self.guitar()

                elif fingers == [0,0,0,0,1]:
                    length, img, lineInfo = self.detector.findDistance(16, 20, img)
                    if length > 60:
                        if self.exit_timer == 0:
                            print("exiting")
                            exit()

                elif all(lmlist[i][2] > 0 for i in [8, 12, 16, 20]):
                    cursor_x = np.interp(x3, (frameR, self.width - frameR), (0, self.screen_width))
                    cursor_y = np.interp(y3, (frameR, self.height - frameR), (0, self.screen_height))

                    self.curr_x = self.prev_x + (cursor_x - self.prev_x) / self.smoothening
                    self.curr_y = self.prev_y + (cursor_y - self.prev_y) / self.smoothening

                    # Check if sliding left and movement surpasses the threshold
                    if self.curr_x < self.prev_x and abs(self.curr_x - self.prev_x) > self.x_threshold:
                        self.slide_counter_left += 1
                        self.slide_counter_right = 0
                        if self.slide_counter_left > 6:
                            if self.slide_timer == 0:
                                self.perform_slide_left() 
                            self.slide_counter_left = 0
                    elif self.curr_x > self.prev_x and abs(self.curr_x - self.prev_x) > self.x_threshold:
                        self.slide_counter_right += 1
                        self.slide_counter_left = 0
                        if self.slide_counter_right > 6:
                            if self.slide_timer == 0:
                                self.perform_slide_right()
                            self.slide_counter_right = 0 
                            
                            
                    self.prev_x, self.prev_y = self.curr_x, self.curr_y

                elif fingers == [1,1,0,0,1]:    
                    if self.record_timer == 0:
                        self.perform_record()

            cTime = time.time()
            fps = 1/(cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        
            self.click_timer = max(0, self.click_timer - 1)
            self.right_click_timer = max(0, self.right_click_timer - 1)
            self.record_timer = max(0, self.record_timer - 1)
            self.slide_timer = max(0, self.slide_timer - 1)
            self.exit_timer = max(0, self.exit_timer - 1)
if __name__ == "__main__":
    vm = VirtualMouse()
    vm.run()
