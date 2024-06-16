import cv2
import matplotlib.pyplot as plt
import os

# Detect faces in an image:

# Algorithm
alg = os.path.dirname(os.path.realpath(__file__)) + '/haarcascade_frontalface_default.xml'

# Path to the image
imagePath = 'image.jpg'

# Load the image
img = cv2.imread(imagePath)

# Convert the image to gray scale
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load the classifier and create a cascade object for face detection
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + alg
)

# Detect faces in the image
face = face_classifier.detectMultiScale(
    gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
)

# Draw a rectangle around the faces
for (x, y, w, h) in face:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)

# Convert the image to RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Display the image using matplotlib
plt.figure(figsize=(20,10))
plt.imshow(img_rgb)
plt.axis('off')

# Uncomment the line below to display the image
# plt.show()