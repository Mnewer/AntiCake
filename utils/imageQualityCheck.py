import cv2
import numpy as np
import os

# Check the quality of images and remove the ones that are not clear
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages/')

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()

def select_best_images(directory, sharpness_threshold):
    best_images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # read in grayscale mode
            laplacian_variance = variance_of_laplacian(image)
            if laplacian_variance > sharpness_threshold:  # compare with a sharpness threshold
                print(f"Image: {filename}, Laplacian Variance: {laplacian_variance}")
                best_images.append(image_path)
            
    # uncomment to remove the images not in the best_images list
    # deletes the images not in the best_images list
    # for filename in os.listdir(directory):
    #     if filename.endswith(".jpg") or filename.endswith(".png"):
    #         image_path = os.path.join(directory, filename)
    #         if image_path not in best_images:
    #             os.remove(image_path)
    return best_images

# Set a specific sharpness threshold based on your observations
sharpness_threshold = 500.0  # higher variance indicates sharper image with more details and edges
best_images = select_best_images(path, sharpness_threshold)
print(f"Selected best images: {best_images}")