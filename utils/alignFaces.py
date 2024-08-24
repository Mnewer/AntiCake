import os
import cv2
import numpy as np

# Load the Haar cascade xml files for face and eye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Directory containing images
images_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages')

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def remove_unclear_images(directory, sharpness_threshold):
    removed_count = 0
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            laplacian_variance = variance_of_laplacian(image)
            if laplacian_variance <= sharpness_threshold:
                os.remove(image_path)
                removed_count += 1
                print(f"Removed: {filename}, Laplacian Variance: {laplacian_variance}")
    
    return removed_count

def remove_undetectable_faces(directory):
    removed_count = 0

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 0:
                os.remove(image_path)
                removed_count += 1
                print(f"Removed: {filename} (no face detected)")

    return removed_count

def align_faces(directory):
    aligned_count = 0

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)

                if len(eyes) >= 2:
                    # Sort eyes by x-coordinate
                    eyes = sorted(eyes, key=lambda e: e[0])
                    
                    # Calculate angle for rotation
                    eye1, eye2 = eyes[:2]
                    dx = eye2[0] - eye1[0]
                    dy = eye2[1] - eye1[1]
                    angle = np.degrees(np.arctan2(dy, dx)) - 180

                    # Rotate image
                    center = (x + w // 2, y + h // 2)
                    M = cv2.getRotationMatrix2D(center, angle, 1.0)
                    aligned = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)

                    # Save aligned image
                    cv2.imwrite(image_path, aligned)
                    aligned_count += 1
                    print(f"Aligned: {filename}")

    return aligned_count

def detectEyes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]