import os
import cv2

# Load the Haar cascade xml files for face and eye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Directory containing images
images_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages')

# Load the Haar cascade xml files for face and eye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Directory containing images
images_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages')

def detectEyes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

def show_images(directory):
    filenames = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    index = 0

    while 0 <= index < len(filenames):
        filename = filenames[index]
        path = os.path.join(directory, filename)
        img = cv2.imread(path)
        if img is not None:
            detectEyes(img)
            # Add descriptive text
            # Prepare the text to be displayed
            instructions = "Press 'A'/'D' to navigate, 'K' to delete image and 'Q' to quit"

            # Set font, scale, color, and thickness for the text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            color = (255, 255, 255)  # White color
            thickness = 2
            line_type = cv2.LINE_AA

            # Get the text size to position it at the bottom of the window
            text_size = cv2.getTextSize(instructions, font, font_scale, thickness)[0]
            text_x = (img.shape[1] - text_size[0]) // 2  # Center the text horizontally
            text_y = img.shape[0] - 10  # Position the text at the bottom of the window

            # Put the text on the frame
            cv2.putText(img, instructions, (text_x, text_y), font, font_scale, color, thickness, line_type)
            cv2.imshow('Image', img)
            key = cv2.waitKey(0) & 0xFF
            
            if key == ord('a'):  # move to the previous image
                index -= 1
            elif key == ord('d'):  # move to the next image
                index += 1
            elif key == ord('q'):  # 'q' pressed
                break
            elif key == ord('k'):  # 'k' pressedd
                os.remove(path)
                print(f"Deleted {filename}")
                filenames.pop(index)  # Remove the filename from the list
                # Do not increment index to account for the removed item
                continue
            else:
                continue  # Handle any other key by simply showing the next image
        else:
            index += 1  # If the image is None, move to the next image

    cv2.destroyAllWindows()

show_images(images_dir)