import cv2

class Camera:
    def __init__(self):
        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not self.cap.isOpened():
            print("Unable to read camera feed")
    
    def open_camera_feed(self):
        while True:
            ret, frame = self.cap.read()
    
            if not ret:
                print("Unable to read camera feed")
                break

            # Basic instructions to be displayed on the screen
            instructions = "Press 'Q' to quit"

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
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    def __del__(self):
        # Release the camera
        self.cap.release()
        cv2.destroyAllWindows()