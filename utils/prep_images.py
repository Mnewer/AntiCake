import cv2
import os
import numpy as np

class PrepImages:
    def __init__(self, image_folder):
        self.image_folder = image_folder

    def variance_of_laplacian(self, image):
        return cv2.Laplacian(image, cv2.CV_64F).var()

    def remove_undetectable_faces(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        removed_count = 0

        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.image_folder, filename)
                img = cv2.imread(image_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) == 0:
                    os.remove(image_path)
                    removed_count += 1
                    print(f"Removed: {filename} (no face detected)")

        return removed_count

    def remove_unclear_images(self, directory, sharpness_threshold):
        removed_count = 0
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(directory, filename)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                laplacian_variance = self.variance_of_laplacian(image)
                if laplacian_variance <= sharpness_threshold:
                    os.remove(image_path)
                    removed_count += 1
                    print(f"Removed: {filename}, Laplacian Variance: {laplacian_variance}")
        
        return removed_count


