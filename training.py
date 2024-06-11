import cv2
import os
import numpy as np

# Path to the directory containing the training images
path = os.path.dirname(os.path.realpath(__file__)) + '/trainingImages'

# Initialize the face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Initialize an array to hold the training images and labels
images = []
labels = []

# Iterate over the training images
for filename in os.listdir(path):
    if filename.endswith('.jpg'):  # assuming the images are in jpg format
        # Read the image
        img = cv2.imread(os.path.join(path, filename), cv2.IMREAD_GRAYSCALE)
        
        # Resize the image
        img = cv2.resize(img, (200, 200))
        
        # Add the image and label to the arrays
        images.append(np.array(img, 'uint8'))
        labels.append(1)  # assuming all training images are of your face

# Train the face recognizer
face_recognizer.train(images, np.array(labels))

# Save the trained model
face_recognizer.save('trained_model.yml')

# Print a message to indicate that the training is complete
print('Training complete!')