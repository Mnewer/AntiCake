import cv2
import numpy as np
import os

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
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