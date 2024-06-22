import os
import cv2

# Load the Haar cascade xml files for face and eye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Directory containing images
images_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages')

def detectEyes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

import os
import cv2

# Load the Haar cascade xml files for face and eye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Directory containing images
images_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages')

def detectEyes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

def show_images(directory):
    filenames = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    index = 0

    while 0 <= index < len(filenames):
        filename = filenames[index]
        path = os.path.join(directory, filename)
        img = cv2.imread(path)
        if img is not None:
            detectEyes(img)
            # Add descriptive text
            cv2.putText(img, "Use 'A/D' keys to navigate, 'Q' to quit, 'K' to delete", (20, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.7, (0,255,0), 6)
            cv2.imshow('Image', img)
            key = cv2.waitKey(0) & 0xFF
            
            if key == ord('a'):  # move to the previous image
                index -= 1
            elif key == ord('d'):  # move to the next image
                index += 1
            elif key == ord('q'):  # 'q' pressed
                break
            elif key == ord('k'):  # 'k' pressed
                os.remove(path)
                print(f"Deleted {filename}")
                filenames.pop(index)  # Remove the filename from the list
                # Do not increment index to account for the removed item
                continue
            else:
                continue  # Handle any other key by simply showing the next image
        else:
            index += 1  # If the image is None, move to the next image

    cv2.destroyAllWindows()

show_images(images_dir)