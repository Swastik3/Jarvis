import cv2
import time

print("loading cascade files")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
print("cascade files loaded")


width = 640             # Width of Camera
height = 480

pTime = 0        # Used to calculate frame rate

detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)

def detect_eyes(img, classifier, face_coords):
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

def detect_faces(img,classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = classifier.detectMultiScale(gray_frame, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        print("multiple coords")
    elif len(coords) == 1:
        biggest = coords[0]
    else:
        return None
    (x, y, w, h) = biggest
    return (x,y,x + w,y + h)



def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)
    return img

def blob_process(img, detector, eye_coords, threshold=42):
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

def main():
    print("loading camera")
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    cv2.createTrackbar('threshold', 'image', 0, 255, lambda x:None)
    print("camera loaded")
    while True:
        _, frame = cap.read()
        face_coords = detect_faces(frame, face_cascade)
        if face_coords is not None:
            eyes = detect_eyes(frame, eye_cascade, face_coords)
            for eye in eyes:
                if eye is not None:
                    cv2.rectangle(frame,eye[:2],eye[2:],(0,255,0),2)
                    """print("cutting eyebrows")
                    eye = cut_eyebrows(eye)
                    print("blob processing")
                    """
                    threshold = cv2.getTrackbarPos('threshold', 'image')
                    pupil_coords = blob_process(frame, detector, eye, threshold)
                    if pupil_coords is not None:
                        pupil_x, pupil_y = pupil_coords
                        cv2.circle(frame, (int(pupil_x), int(pupil_y)), 10, (0, 0, 255), 2)
            
            #cv2.rectangle(frame,face_coords[:2],face_coords[2:],(0,255,0),2)
        cv2.imshow('image', frame)
        #time.sleep(0.05) # 20 fps
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
