import cv2
import os

# Load the Haar cascade xml files for face and eye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages/')

# remove images that do not register a face
for filename in os.listdir(path):
    if filename.endswith('.jpg'):
        img = cv2.imread(os.path.join(path, filename))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            os.remove(os.path.join(path, filename))
            print('Removed:', filename)
    else:
        continue

print('Done')
