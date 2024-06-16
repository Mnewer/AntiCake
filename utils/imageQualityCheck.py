import cv2
import numpy as np
import os

# Check the quality of images and remove the ones that are not clear
path = os.path.dirname(os.path.realpath(__file__)) + '/trainingImages'

def variance_of_laplacian(image):
    # convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def select_best_images(directory, threshold):
    best_images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            image = cv2.imread(image_path)
            if variance_of_laplacian(image) > threshold:
                best_images.append(image_path)
            
    # uncomment to remove the images not in the best_images list
    # deletes the images not in the best_images list
    # for filename in os.listdir(directory):
    #     if filename.endswith(".jpg") or filename.endswith(".png"):
    #         image_path = os.path.join(directory, filename)
    #         if image_path not in best_images:
    #             os.remove(image_path)
    return best_images


print(select_best_images(path, 100))