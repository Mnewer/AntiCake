import cv2
import os

class Camera:
    def __init__(self):
        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not self.cap.isOpened():
            print("Unable to read camera feed")
    

    def _open_camera_feed(self, instructions: str = "Press 'Q' to quit", path: str = None):
        """
        Opens the camera feed and displays the frames.

        Args:
            instructions (str, optional): Instructions to be displayed on the frame. Defaults to "Press 'Q' to quit".
            path (str, optional): Path to save captured images. Defaults to None.

        Returns:
            None
        """

        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Unable to read camera feed")
                break

            # Set font, scale, color, and thickness for the text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (255, 255, 255)
            thickness = 2
            line_type = cv2.LINE_AA

            # Text coordinates, starting from the top-left corner
            text_x = 10
            text_y = 25

            # Put the text on the frame
            cv2.putText(frame, instructions, (text_x, text_y), font, font_scale, color, thickness, line_type)

            # Display the resulting frame
            cv2.imshow('frame', frame)

            # Press 'q' on keyboard to exit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c') and path is not None:
                self._capture_image(frame, path)


    def _capture_image(self, frame, path):
        """
        Captures and saves an image from the camera feed.

        Args:
            frame: The current frame from the camera feed.
            path: The directory path where the image will be saved.

        Returns:
            None
        """
        # Check the last captured frame number by counting the number of files in the directory and incrementing by 1
        frame_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]) + 1
            
        # Ensure the filename is unique to avoid overwriting
        while os.path.exists(os.path.join(path, f'frame{frame_count}.jpg')):
            frame_count += 1
        ret, frame = self.cap.read() 
        cv2.imwrite(os.path.join(path, f'frame{frame_count}.jpg'), frame)
        print(f"Image saved as frame{frame_count}.jpg")
        frame_count += 1
    
    def capture_image(self, path = "trainingImages"):
            """
            Captures an image from the camera feed and saves it to the specified path.

            Args:
                path (str): The path where the captured image will be saved.

            Returns:
                None
            """
            # Method specific instructions:
            instructions = "Press 'C' to capture, 'Q' to quit"
            self._open_camera_feed(instructions, path)


    def close(self):
        """
        Closes the camera feed and releases resources.

        This method ensures that the camera is properly closed and all OpenCV windows are destroyed.
        It should be called when the camera object is no longer needed.

        Returns:
            None
        """
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        
                
    def __del__(self):
        self.close()