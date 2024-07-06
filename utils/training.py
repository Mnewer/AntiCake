import cv2
import os
import numpy as np

# Path to the directory containing the training images
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages')

img = cv2.imread(os.path.join(path, '1.jpg'), cv2.IMREAD_GRAYSCALE)
img = cv2.equalizeHist(img)

# alg = "haarcascade_frontalface_default.xml"
alg = "haarcascade_frontalcatface_extended.xml"

# Initialize the face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
# face_recognizer = cv2.face.FisherFaceRecognizer_create()

# Initialize the face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# faces = face_cascade.detectMultiScale(img, scaleFactor=1.05, minNeighbors=5)
# faces = face_cascade.detectMultiScale(img, scaleFactor=1.05, minNeighbors=3)

# Initialize arrays to hold the training images and labels
images = []
labels = []

# Label counter for assigning unique labels to each individual
label_counter = 0
label_dict = {}

# Iterate over the training images
for filename in os.listdir(path):
    if filename.endswith('.jpg'):  # assuming the images are in jpg format
        # Read the image
        img = cv2.imread(os.path.join(path, filename), cv2.IMREAD_GRAYSCALE)
        
        # Detect faces in the image
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
        
        # If faces are found
        for (x, y, w, h) in faces:
            # Extract the face region
            face = img[y:y+h, x:x+w]
            
            # Resize the face region to a fixed size
            face = cv2.resize(face, (200, 200))
            
            # Check if the filename is already in the label dictionary
            if filename not in label_dict:
                label_dict[filename] = label_counter
                label_counter += 1
            
            # Add the face and corresponding label to the arrays
            images.append(np.array(face, 'uint8'))
            labels.append(label_dict[filename])

            flipped_face = cv2.flip(face, 1)
            images.append(np.array(flipped_face, 'uint8'))
            labels.append(label_dict[filename])

assert len(images) == len(labels), "The number of images and labels should be the same!"

for img in images:
    assert len(img.shape) == 2, "The images should be 2D arrays!"

# Train the face recognizer
if images and labels:
    face_recognizer.train(images, np.array(labels))

# Save the trained model
face_recognizer.save('model/trained_model.yml')

# Print a message to indicate that the training is complete
print('Training complete!')