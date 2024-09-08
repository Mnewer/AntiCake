# import cv2
# import os

# def remove_undetectable_faces(directory):
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     removed_count = 0

#     for filename in os.listdir(directory):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#             image_path = os.path.join(directory, filename)
#             img = cv2.imread(image_path)
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#             if len(faces) == 0:
#                 os.remove(image_path)
#                 removed_count += 1
#                 print(f"Removed: {filename} (no face detected)")

#     return removed_count