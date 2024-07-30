import cv2
import matplotlib.pyplot as plt

def main():

    # Load the classifier and create a cascade object for face detection
    # alg = "haarcascade_frontalface_default.xml"'
    alg = "haarcascade_frontalcatface_extended.xml"


    # Load the classifier and create a cascade object for face detection
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + alg
    ) 


    # Get the model type from the trained model
    model = 'model/trained_model.yml'
    with open(model, 'r') as f:
        model_info = f.read()
        model_type = model_info.split('\n')[2]


    # initialize the face recognizer based on the model type
    if "opencv_fisherfaces" in model_type:
        print("Fisher")
        face_recognizer = cv2.face.FisherFaceRecognizer_create()
    elif "opencv_lbphfaces" in model_type:
        print("LBPH")
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    else:
        raise ValueError("Invalid model type")


    # Load the trained model
    face_recognizer.read(model)


    # Video capture
    video_capture = cv2.VideoCapture(0)


    #label for my face
    MY_FACE_LABEL = 1


    # Load the classifier and create a cascade object for face detection'
    def detect_bounding_box(vid):
        gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
        for (x, y, w, h) in faces:
            face = gray_image[y:y+h, x:x+w]
            # face = cv2.resize(face, (200, 200))
            label, confidence = face_recognizer.predict(face)
            if label == MY_FACE_LABEL and confidence < 100:
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
        )
        cv2.imshow(
            "AntiCake Project", video_frame
        )  # display the video frame in a window
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()