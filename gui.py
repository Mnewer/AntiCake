import tkinter as tk
from tkinter import messagebox, ttk
from utils import imageQualityCheck, removeUndetectable, alignFaces
import os
import cv2
import numpy as np
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.image_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'trainingImages')
        self.current_image = None
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_recognizer.read('model/trained_model.yml')  # Load your trained model
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.update_quality_info()
        self.select_first_image()

    def create_widgets(self):
        # Column 1: Image preview and navigation
        self.column1 = tk.Frame(self, width=400, height=500)
        self.column1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.column1.grid_propagate(False)

        self.column1_header = tk.Label(self.column1, text="Image Preview", font=("Arial", 12, "bold"))
        self.column1_header.grid(row=0, column=0, pady=(0, 10))

        self.image_frame = tk.Frame(self.column1, width=400, height=400)
        self.image_frame.grid(row=1, column=0, pady=(0, 10))
        self.image_frame.grid_propagate(False)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        self.nav_frame = tk.Frame(self.column1)
        self.nav_frame.grid(row=2, column=0)

        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.prev_image_wrap)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(self.nav_frame, text="Delete", command=self.delete_current_image, fg="red")
        self.delete_button.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(self.nav_frame, text="Next", command=self.next_image_wrap)
        self.next_button.grid(row=0, column=2, padx=5)

        # Column 2: Image quality info
        self.column2 = tk.Frame(self)
        self.column2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.column2_header = tk.Label(self.column2, text="Image Quality Information", font=("Arial", 12, "bold"))
        self.column2_header.pack(pady=(0, 10))

        self.quality_frame = ttk.LabelFrame(self.column2, text="Image Quality Info")
        self.quality_frame.pack(fill=tk.BOTH, expand=True)

        self.quality_tree = ttk.Treeview(self.quality_frame, columns=('Filename', 'Laplacian', 'Face Detected'), show='headings')
        self.quality_tree.heading('Filename', text='Filename')
        self.quality_tree.heading('Laplacian', text='Laplacian Value')
        self.quality_tree.heading('Face Detected', text='Face Detected')
        self.quality_tree.column('Filename', width=150)
        self.quality_tree.column('Laplacian', width=100)
        self.quality_tree.column('Face Detected', width=100)
        self.quality_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.quality_scrollbar = ttk.Scrollbar(self.quality_frame, orient="vertical", command=self.quality_tree.yview)
        self.quality_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.quality_tree.configure(yscrollcommand=self.quality_scrollbar.set)
        self.quality_tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # Column 3: Controls
        self.column3 = tk.Frame(self)
        self.column3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.column3_header = tk.Label(self.column3, text="Controls", font=("Arial", 12, "bold"))
        self.column3_header.pack(pady=(0, 10))

        self.capture_button = tk.Button(self.column3, text="Capture images", command=self.capture_image)
        self.capture_button.pack(fill=tk.X, pady=5)

        self.threshold_frame = tk.Frame(self.column3)
        self.threshold_frame.pack(fill=tk.X, pady=5)

        self.threshold_label = tk.Label(self.threshold_frame, text="Threshold:")
        self.threshold_label.pack(side=tk.LEFT)

        self.threshold_input = tk.Entry(self.threshold_frame, width=5)
        self.threshold_input.pack(side=tk.LEFT, padx=5)
        self.threshold_input.insert(0, "500")

        self.remove_unclear_button = tk.Button(self.column3, text="Remove unclear images", command=self.remove_unclear_images)
        self.remove_unclear_button.pack(fill=tk.X, pady=5)

        self.prep_images_button = tk.Button(self.column3, text="Prep Images", command=self.prep_images)
        self.prep_images_button.pack(fill=tk.X, pady=5)

        self.train_button = tk.Button(self.column3, text="Train model", command=self.train_model)
        self.train_button.pack(fill=tk.X, pady=5)

        # Add the Live Preview button here
        self.live_preview_button = tk.Button(self.column3, text="Live Preview", command=self.open_live_preview)
        self.live_preview_button.pack(fill=tk.X, pady=5)

        # Create a frame to push the QUIT button to the bottom
        self.spacer_frame = tk.Frame(self.column3)
        self.spacer_frame.pack(fill=tk.BOTH, expand=True)

        # Move the QUIT button to the bottom
        self.quit = tk.Button(self.column3, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(fill=tk.X, pady=5, side=tk.BOTTOM)

    def update_quality_info(self):
        self.quality_tree.delete(*self.quality_tree.get_children())
        for filename in sorted(os.listdir(self.image_folder)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.image_folder, filename)
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                laplacian_variance = imageQualityCheck.variance_of_laplacian(gray)
                
                # Detect face
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                face_detected = "Yes" if len(faces) > 0 else "No"
                
                self.quality_tree.insert('', 'end', values=(filename, f"{laplacian_variance:.2f}", face_detected))

    def select_first_image(self):
        if self.quality_tree.get_children():
            first_item = self.quality_tree.get_children()[0]
            self.quality_tree.selection_set(first_item)
            self.quality_tree.focus(first_item)
            self.on_tree_select(None)

    def on_tree_select(self, event):
        selected_items = self.quality_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            filename = self.quality_tree.item(selected_item)['values'][0]
            self.display_image(filename)
            self.quality_tree.see(selected_item)  # Ensure the selected item is visible

    def display_image(self, filename):
        image_path = os.path.join(self.image_folder, filename)
        image = Image.open(image_path)
        image.thumbnail((380, 380))  # Resize image to fit in the frame
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.current_image = filename

    def prev_image_wrap(self):
        current_index = self.get_current_index()
        if current_index > 0:
            prev_item = self.quality_tree.get_children()[current_index - 1]
        else:
            prev_item = self.quality_tree.get_children()[-1]  # Wrap to the last item
        self.quality_tree.selection_set(prev_item)
        self.quality_tree.focus(prev_item)
        self.quality_tree.see(prev_item)  # Ensure the item is visible
        self.on_tree_select(None)

    def next_image_wrap(self):
        current_index = self.get_current_index()
        if current_index < len(self.quality_tree.get_children()) - 1:
            next_item = self.quality_tree.get_children()[current_index + 1]
        else:
            next_item = self.quality_tree.get_children()[0]  # Wrap to the first item
        self.quality_tree.selection_set(next_item)
        self.quality_tree.focus(next_item)
        self.quality_tree.see(next_item)  # Ensure the item is visible
        self.on_tree_select(None)

    def get_current_index(self):
        selected_items = self.quality_tree.selection()
        if selected_items:
            return self.quality_tree.index(selected_items[0])
        return -1

    def remove_unclear_images(self):
        try:
            threshold = int(self.threshold_input.get())
            removed_count = imageQualityCheck.remove_unclear_images(self.image_folder, threshold)
            messagebox.showinfo("Remove Unclear Images", f"Removed {removed_count} unclear images.")
            self.update_quality_info()
            self.select_first_image()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid threshold value.")

    def prep_images(self):
        removed_count = removeUndetectable.remove_undetectable_faces(self.image_folder)
        aligned_count = alignFaces.align_faces(self.image_folder)
        messagebox.showinfo("Prep Images", f"Removed {removed_count} images without detectable faces.\nAligned {aligned_count} faces.")
        self.update_quality_info()
        self.select_first_image()

    def capture_image(self):
        # Implement image capture functionality
        pass

    def train_model(self):
        # Implement model training functionality
        pass

    def delete_current_image(self):
        if self.current_image:
            if messagebox.askyesno("Delete Image", f"Are you sure you want to delete {self.current_image}?"):
                os.remove(os.path.join(self.image_folder, self.current_image))
                self.update_quality_info()
                self.select_first_image()
                messagebox.showinfo("Delete Image", f"{self.current_image} has been deleted.")

    def open_live_preview(self):
        preview_window = tk.Toplevel(self.master)
        preview_window.title("Live Preview")
        preview_window.geometry("640x480")

        video_frame = tk.Label(preview_window)
        video_frame.pack()

        cap = cv2.VideoCapture(0)

        def update_frame():
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    label, confidence = self.face_recognizer.predict(face_roi)

                    if label == 1:  # Assuming label 1 is the face we're looking for
                        color = (0, 255, 0)  # Green
                    else:
                        color = (0, 0, 255)  # Red

                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, f"Confidence: {confidence:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                video_frame.imgtk = imgtk
                video_frame.configure(image=imgtk)
                video_frame.after(10, update_frame)
            else:
                cap.release()

        update_frame()

        def on_closing():
            cap.release()
            preview_window.destroy()

        preview_window.protocol("WM_DELETE_WINDOW", on_closing)