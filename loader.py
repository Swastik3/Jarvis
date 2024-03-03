from threading import Thread
import cv2
import time
from VirtualMouse import VirtualMouse

def play_video():
    cap = cv2.VideoCapture("./vid.mp4")
    cv2.namedWindow("Video Player", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video Player", 1280, 720)

    while (cap.isOpened()):
        success, frame = cap.read()
        if success:
            cv2.imshow('Video Player', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):  # wait for a key press for 25 ms
                break
        else:
            print("Video ended")
            break
    
    cap.release()
    cv2.destroyAllWindows()

t1 = Thread(target=play_video)
t1.start()
vm = VirtualMouse()
vm.run()