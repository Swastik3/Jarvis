import cv2
import time

print("loading cascade files")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
print("cascade files loaded")

class EyeTracker():
    def __init__(self,window_name) -> None:
        self.width = 640
        self.height = 480
        self.debug_flag = False
        self.window_name = window_name
        
        print("loading video input")
        self.cap = cv2.VideoCapture(0)
        print("video input loaded")
        
        detector_params = cv2.SimpleBlobDetector_Params()
        detector_params.filterByArea = True
        detector_params.maxArea = 1500
        self.detector = cv2.SimpleBlobDetector_create(detector_params)
        
        cv2.createTrackbar('threshold', self.window_name, 0, 255, lambda x:None)
        cv2.createTrackbar('debug', self.window_name, 0, 1, self.debug_toggle)

    def detect_eyes(self,img, classifier, face_coords):
        assert face_coords is not None
        x_top,y_top,x_bottom,y_bottom = face_coords
        face_frame = img[face_coords[1]:face_coords[3], face_coords[0]:face_coords[2]]
        
        gray_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2GRAY)
        eyes = classifier.detectMultiScale(gray_frame, 1.3, 5) # detect eyes
        width = x_bottom - x_top # get face frame width
        height = y_bottom - y_top # get face frame height
        
        assert width > 0 and height > 0
        
        left_eye_coords = None
        right_eye_coords = None
        
        for (x, y, w, h) in eyes:
            if y > height / 2:
                pass
            eyecenter = x + w / 2  # get the eye center
            if eyecenter < width * 0.5:
                left_eye_coords = (x_top + x, y_top + y, x_top + x + w, y_top + y + h)
            else:
                right_eye_coords = (x_top + x, y_top + y, x_top + x + w, y_top + y + h)
        return left_eye_coords, right_eye_coords

    def detect_faces(self,img,classifier):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coords = classifier.detectMultiScale(gray_frame, 1.3, 5)
        if len(coords) > 1:
            biggest = (0, 0, 0, 0)
            for i in coords:
                if i[3] > biggest[3]:
                    biggest = i
            #print("multiple coords")
        elif len(coords) == 1:
            biggest = coords[0]
        else:
            return None
        (x, y, w, h) = biggest
        return (x,y,x + w,y + h)

    def apply_filter(self,img,threshold):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        img = cv2.erode(img, None, iterations=2) #1
        img = cv2.dilate(img, None, iterations=4) #2
        img = cv2.medianBlur(img, 5)
        return img

    def cut_eyebrows(self,img):
        height, width = img.shape[:2]
        eyebrow_h = int(height / 4)
        img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)
        return img

    def blob_process(self,img, detector, eye_coords, threshold=42):
        x_top,y_top,x_bottom,y_bottom = eye_coords
        
        eye_frame = img[y_top:y_bottom, x_top:x_bottom]
        gray_frame = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
        img = cv2.erode(img, None, iterations=2) #1
        img = cv2.dilate(img, None, iterations=4) #2
        img = cv2.medianBlur(img, 5) #3
        
        #cv2.imshow('tmp_img', img)
        #time.sleep(1)
        
        keypoints = detector.detect(img)
        if len(keypoints) > 0:
            detected_x, detected_y = keypoints[0].pt
            return (detected_x + x_top).item(), (detected_y + y_top).item()
        else:
            return None

    def debug_toggle(self,x):
        self.debug_flag = not self.debug_flag

    def track_eye_step(self):
        threshold = cv2.getTrackbarPos('threshold', self.window_name)
        _, frame = self.cap.read()
        face_coords = self.detect_faces(frame, face_cascade)
        if face_coords is not None:
            eyes = self.detect_eyes(frame, eye_cascade, face_coords)
            for eye in eyes:
                if eye is not None:
                    cv2.rectangle(frame,eye[:2],eye[2:],(0,255,0),2)
                    """print("cutting eyebrows")
                    eye = cut_eyebrows(eye)
                    print("blob processing")
                    """
                    
                    pupil_coords = self.blob_process(frame, self.detector, eye, threshold)
                    if pupil_coords is not None:
                        pupil_x, pupil_y = pupil_coords
                        cv2.circle(frame, (int(pupil_x), int(pupil_y)), 10, (0, 0, 255), 2)
        if self.debug_flag:
            frame = self.apply_filter(frame, threshold)
        cv2.imshow(self.window_name, frame)

def main():
    
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    tracker = EyeTracker("Image")
    while True:
        tracker.track_eye_step()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
