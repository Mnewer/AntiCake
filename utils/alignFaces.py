import os
import cv2

# Load the Haar cascade xml files for face and eye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# path = os.path.dirname(os.path.realpath(__file__)) + 'trainingImages/frame192'
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages/frame458.jpg')

print(path)

def detectEyes(img):

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    #crop the face
    # for (x, y, w, h) in faces:
    #     img = img[y:y+h, x:x+w]
    #     break

    # Loop through the faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Get the region of interest (the face)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        # Detect eyes
        eyes = eye_cascade.detectMultiScale(roi_gray)
        # Loop through the eyes
        for (ex, ey, ew, eh) in eyes:
            # Draw a rectangle around the eyes
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)



    # Display the image
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detectEyes(cv2.imread(path))