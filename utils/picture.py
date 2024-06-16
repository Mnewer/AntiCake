import cv2
import time
import os

# Path to the directory containing the training images
path = os.path.dirname(os.path.realpath(__file__)) + '/trainingImages'

# Create the directory if it does not exist
if not os.path.exists(path):
    os.makedirs(path)

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Unable to read camera feed")

# Update the counter continue to save more images
frame_count = 561
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Save frame every second (assuming 30 frames per second)
        # if frame_count % 30 == 0:
            # Then, in the loop:
        cv2.imwrite(os.path.join(path, 'frame%d.jpg' % frame_count), frame)

        frame_count += 1
    else:
        break

    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Pause for 1 second
    time.sleep(1)

# When everything done, release the video capture and video write objects
cap.release()

# Closes all the frames
cv2.destroyAllWindows()