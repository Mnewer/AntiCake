import cv2
import time
import os

# Path to the directory containing the training images
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trainingImages')

# Create the directory if it does not exist
if not os.path.exists(path):
    os.makedirs(path)

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Unable to read camera feed")

# Check the last captured frame number by counting the number of files in the directory and incrementing by 1
frame_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]) + 1

while True:
    ret, frame = cap.read()

    if not ret:
        print("Unable to read camera feed")
        break


    # Prepare the text to be displayed
    instructions = "Press 'C' to capture, 'Q' to quit"

    # Set font, scale, color, and thickness for the text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    color = (255, 255, 255)  # White color
    thickness = 2
    line_type = cv2.LINE_AA

    # Get the text size to position it at the bottom of the window
    text_size = cv2.getTextSize(instructions, font, font_scale, thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2  # Center the text horizontally
    text_y = frame.shape[0] - 10  # Position the text at the bottom of the window

    # Put the text on the frame
    cv2.putText(frame, instructions, (text_x, text_y), font, font_scale, color, thickness, line_type)


    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Press 'c' on keyboard to capture an image
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # Ensure the filename is unique to avoid overwriting
        while os.path.exists(os.path.join(path, f'frame{frame_count}.jpg')):
            frame_count += 1
        cv2.imwrite(os.path.join(path, f'frame{frame_count}.jpg'), frame)
        print(f"Image saved as frame{frame_count}.jpg")
        frame_count += 1

    # Press 'q' on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the video capture and video write objects
cap.release()

# Closes all the frames
cv2.destroyAllWindows()