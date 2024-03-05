from threading import Thread
import cv2
import time
from VirtualMouse import VirtualMouse


def play_video():
    cap = cv2.VideoCapture("./vid.mp4")

    while (cap.isOpened()):  # Stop the video if checker is true
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
t1.join()

vm.run()

# If checker becomes true, wait for the video thread to finish
