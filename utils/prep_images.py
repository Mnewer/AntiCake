import cv2
import os
import numpy as np

class PrepImages:
    def __init__(self, image_folder, target_size=(224, 224)):
        self.image_folder = image_folder
        self.target_size = target_size  # Target size for resizing

    def variance_of_laplacian(self, image):
        return cv2.Laplacian(image, cv2.CV_64F).var()

    def remove_undetectable_faces(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        removed_count = 0

        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.image_folder, filename)
                img = self.process_image(image_path)
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
                img = self.process_image(image_path)
                laplacian_variance = self.variance_of_laplacian(img)
                if laplacian_variance <= sharpness_threshold:
                    os.remove(image_path)
                    removed_count += 1
                    print(f"Removed: {filename}, Laplacian Variance: {laplacian_variance}")
        
        return removed_count

    def resize_image(self, image):
        return cv2.resize(image, self.target_size)

    def normalize_image(self, image):
        return image / 255.0  # Normalize to [0, 1]

    def augment_image(self, image):
        # Example augmentation: horizontal flip
        if np.random.rand() > 0.5:
            image = cv2.flip(image, 1)
        return image

    def histogram_equalization(self, image):
        return cv2.equalizeHist(image)

    def denoise_image(self, image):
        return cv2.fastNlMeansDenoising(image, None, 30, 7, 21)

    def process_image(self, image_path):
        print("process")
        img = cv2.imread(image_path)
        img = self.resize_image(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for some operations
        img = self.denoise_image(img)
        img = self.histogram_equalization(img)
        img = self.normalize_image(img)
        img = self.augment_image(img)
        return img

    def prepare_images(self, sharpness_threshold):
        print("prep")
        total_removed_faces = self.remove_undetectable_faces()
        total_removed_unclear = self.remove_unclear_images(self.image_folder, sharpness_threshold)
        print(f"Total images removed (no faces detected): {total_removed_faces}")
        print(f"Total unclear images removed: {total_removed_unclear}")

        return total_removed_faces, total_removed_unclear


