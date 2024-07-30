import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from utils import camera

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x600")
        self.cam = camera.Camera()
        self.pack()
        self.create_widgets()
        self.populate_image_list()

    def create_widgets(self):
        self.image_frame = tk.Frame(self)
        self.control_frame = tk.Frame(self)

        self.image_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.control_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.image_preview = tk.Label(self.image_frame, text="Image Preview")
        self.image_preview.grid(row=0, column=0, sticky="nsew")

        self.navigation_frame = tk.Frame(self.image_frame)
        self.navigation_frame.grid(row=1, column=0, sticky="ew")

        self.back_button = tk.Button(self.navigation_frame, text="Back", command=self.show_previous_image)
        self.back_button.pack(side="left")

        self.next_button = tk.Button(self.navigation_frame, text="Next", command=self.show_next_image)
        self.next_button.pack(side="right")

        self.image_list = tk.Listbox(self)
        self.image_list.grid(row=0, column=1, sticky="nsew")
        self.image_list.bind("<<ListboxSelect>>", self.on_image_select)

        self.extra_frame = tk.Frame(self)
        self.extra_frame.grid(row=0, column=2, rowspan=2, sticky="nsew")

        self.quit = tk.Button(self.extra_frame, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        # Configure grid weights to make the layout responsive
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

    def populate_image_list(self):
        """
        Populates the image list in the GUI with image files from the specified folder.

        This method retrieves image files from the 'trainingImages' folder and adds them to the image list in the GUI.
        Only files with the extensions '.png', '.jpg', '.jpeg', '.gif', and '.bmp' are considered as image files.

        If the 'trainingImages' folder exists, the method retrieves the image files and inserts their names into the image list.
        The first image in the list is shown as the default image if there are any images available.

        Args:
            None

        Returns:
            None
        """
        image_folder = "trainingImages"
        image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp")
        
        if os.path.exists(image_folder):
            self.images = [file_name for file_name in os.listdir(image_folder) if file_name.lower().endswith(image_extensions)]
            for file_name in self.images:
                self.image_list.insert(tk.END, file_name)
            
            # Show the first image as default if there are images
            if self.images:
                self.current_image_index = 0
                self.show_image(self.images[self.current_image_index])

    def on_image_select(self, event):
        """
        Event handler for when an image is selected from the image list.

        Parameters:
        - event: The event object representing the selection event.

        Returns:
        None
        """
        selected_index = self.image_list.curselection()
        if selected_index:
            self.current_image_index = selected_index[0]
            selected_image = self.image_list.get(selected_index)
            self.show_image(selected_image)

    def show_image(self, image_name):
        """
        Displays the specified image in the image preview box.

        Parameters:
        - image_name (str): The name of the image file to display.

        Returns:
        None
        """
        image_folder = "trainingImages"
        image_path = os.path.join(image_folder, image_name)
        image = Image.open(image_path)
        image = image.resize((400, 300), Image.LANCZOS)  # Resize the image to fit the preview box
        photo = ImageTk.PhotoImage(image)

        self.image_preview.config(image=photo)
        self.image_preview.image = photo  # Keep a reference to avoid garbage collection

        # Highlight the current image in the list
        self.image_list.selection_clear(0, tk.END)
        self.image_list.selection_set(self.current_image_index)
        self.image_list.see(self.current_image_index)

    def show_previous_image(self):
        """
        Displays the previous image in the list of images.

        If there are no images, nothing will be displayed.

        The current image index is decremented by 1 and wrapped around to the end of the list if necessary.
        The updated current image is then displayed using the `show_image` method.
        """
        if self.images:
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
            self.show_image(self.images[self.current_image_index])

    def show_next_image(self):
        """
        Displays the next image in the list of images.

        If there are no images, nothing will be displayed.

        The current image index is incremented by 1 and wrapped around to the start of the list if necessary.
        The updated current image is then displayed using the `show_image` method.
        """
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.show_image(self.images[self.current_image_index])

