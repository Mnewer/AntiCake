import cv2
import matplotlib.pyplot as plt


# Path to the image
imagePath = 'image.jpg'

# Load the image
img = cv2.imread(imagePath)

# Convert the image to gray scale
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load the classifier and create a cascade object for face detection
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Load the classifier and create a cascade object for face detection
# def detect_bounding_box(vid):
#     gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
#     faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
#     for (x, y, w, h) in faces:
#         cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
#     return faces

#initialize the face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

#load the trained model
face_recognizer.read('trained_model.yml')

# Video capture
video_capture = cv2.VideoCapture(0)

#label for my face
MY_FACE_LABEL = 1

#Load the classifier and create a cascade object for face detection
def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        face = gray_image[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face)
        if label == MY_FACE_LABEL and confidence < 75:
            print('My face detected with confidence:', confidence)
            cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        else:
            # print('Face detected with confidence:', confidence)
            cv2.rectangle(vid, (x, y), (x + w, y + h), (255, 0, 0), 4)
    return faces

# Read the video frame by frame
while True:

    result, video_frame = video_capture.read()  # read frames from the video
    if result is False:
        break  # terminate the loop if the frame is not read successfully

    faces = detect_bounding_box(
        video_frame
    )  # apply the function we created to the video frame

    cv2.imshow(
        "My Face Detection Project", video_frame
    )  # display the processed frame in a window named "My Face Detection Project"

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()