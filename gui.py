import tkinter as tk
from tkinter import messagebox, ttk
from utils import imageQualityCheck, removeUndetectable, alignFaces
import os
import cv2
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.image_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'trainingImages')
        self.current_image = None
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.update_quality_info()
        self.select_first_image()

    def create_widgets(self):
        # Column 1: Image preview and navigation
        self.column1 = tk.Frame(self, width=400, height=500)
        self.column1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.column1.grid_propagate(False)

        self.image_frame = tk.Frame(self.column1, width=400, height=400)
        self.image_frame.grid(row=0, column=0, pady=(0, 10))
        self.image_frame.grid_propagate(False)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        self.nav_frame = tk.Frame(self.column1)
        self.nav_frame.grid(row=1, column=0)

        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.prev_image)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = tk.Button(self.nav_frame, text="Next", command=self.next_image)
        self.next_button.grid(row=0, column=1, padx=5)

        # Column 2: Image quality info
        self.column2 = tk.Frame(self)
        self.column2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.quality_frame = ttk.LabelFrame(self.column2, text="Image Quality Info")
        self.quality_frame.pack(fill=tk.BOTH, expand=True)

        self.quality_tree = ttk.Treeview(self.quality_frame, columns=('Filename', 'Laplacian'), show='headings')
        self.quality_tree.heading('Filename', text='Filename')
        self.quality_tree.heading('Laplacian', text='Laplacian Value')
        self.quality_tree.pack(fill=tk.BOTH, expand=True)
        self.quality_tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # Column 3: Controls
        self.column3 = tk.Frame(self)
        self.column3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

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

        self.quit = tk.Button(self.column3, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(fill=tk.X, pady=5)

    def update_quality_info(self):
        self.quality_tree.delete(*self.quality_tree.get_children())
        for filename in sorted(os.listdir(self.image_folder)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.image_folder, filename)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                laplacian_variance = imageQualityCheck.variance_of_laplacian(image)
                self.quality_tree.insert('', 'end', values=(filename, f"{laplacian_variance:.2f}"))

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

    def display_image(self, filename):
        image_path = os.path.join(self.image_folder, filename)
        image = Image.open(image_path)
        image.thumbnail((380, 380))  # Resize image to fit in the frame
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.current_image = filename

    def prev_image(self):
        current_index = self.get_current_index()
        if current_index > 0:
            prev_item = self.quality_tree.get_children()[current_index - 1]
            self.quality_tree.selection_set(prev_item)
            self.quality_tree.focus(prev_item)
            self.on_tree_select(None)

    def next_image(self):
        current_index = self.get_current_index()
        if current_index < len(self.quality_tree.get_children()) - 1:
            next_item = self.quality_tree.get_children()[current_index + 1]
            self.quality_tree.selection_set(next_item)
            self.quality_tree.focus(next_item)
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