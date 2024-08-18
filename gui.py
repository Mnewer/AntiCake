import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from utils import camera

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1000x400")
        self.pack()
        self.create_widgets()
        self.populate_image_list()
        self.image_folder = "trainingImages"
        self.images = []
        # self.check_for_new_images()

    def create_widgets(self):
        self.frame_image_interaction = tk.Frame(self)

        self.frame_image_interaction.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.image_preview = tk.Label(self.frame_image_interaction, text="Image Preview")
        self.image_preview.grid(row=0, column=0, sticky="nsew")

        # Create a frame for the navigation buttons
        self.frame_navigation = tk.Frame(self.frame_image_interaction)
        self.frame_navigation.grid(row=1, column=0, sticky="ew")

        self.back_button = tk.Button(self.frame_navigation, text="Back", command=self.show_previous_image)
        self.back_button.grid(row=0, column=0, sticky="w")

        self.upload_button = tk.Button(self.frame_navigation, text="Upload", command=self.upload_image)
        self.upload_button.grid(row=0, column=1, sticky="w")

        self.next_button = tk.Button(self.frame_navigation, text="Next", command=self.show_next_image)
        self.next_button.grid(row=0, column=2, sticky="w")

        # Create a listbox to display the image files
        self.image_list = tk.Listbox(self)
        self.image_list.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.image_list.bind("<<ListboxSelect>>", self.on_image_select)


        # Controls frame:
        self.frame_controls = tk.Frame(self)
        self.frame_controls.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=10)

        self.capture_button = tk.Button(self.frame_controls, text="Capture images", command=self.capture_image)
        self.capture_button.pack(side="top", pady=5, anchor="w")

        self.remove_unclear_button = tk.Button(self.frame_controls, text="Remove unclear images")
        self.remove_unclear_button.pack(side="top", pady=5, anchor="w")

        self.prep_images_button = tk.Button(self.frame_controls, text="Prepare images")
        self.prep_images_button.pack(side="top", pady=5, anchor="w")

        self.train_button = tk.Button(self.frame_controls, text="Train model")
        self.train_button.pack(side="top", pady=5, anchor="w")

        self.quit = tk.Button(self.frame_controls, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.threshold_input = tk.Entry(self.frame_controls, width=10)
        self.threshold_label = tk.Label(self.frame_controls, text="Threshold for unclear images:")
        self.threshold_label.pack(side="top", pady=5, anchor="w")

        self.threshold_input.insert(0, "500")
        self.threshold_input.pack(side="top", pady=5, anchor="w")
        

        # Configure grid weights to make the layout responsive
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

    # MARK: Capture image
    def capture_image(self):
        cam = camera.Camera()
        cam.capture_image()

    # MARK: Populate image list
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

    # MARK: Upload image
    def upload_image(self):
        """
        Opens a file dialog to select an image file and copies it to the trainingImages folder.
        Updates the image list, appends the image to the images list, and shows the selected image.

        Returns:
            None
        """
        file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            file_name = os.path.basename(file_path)
            image_folder = "trainingImages"
            image_path = os.path.join(image_folder, file_name)
            # copy the selected image to the trainingImages folder
            try:
                os.makedirs(image_folder, exist_ok=True)
                os.replace(file_path, image_path)
                self.image_list.insert(tk.END, file_name)
                self.images.append(file_name)
                self.current_image_index = len(self.images) - 1
                self.show_image(file_name)
            except OSError as e:
                print(f"Error moving file: {e}")
    

    # MARK: Image selection
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


    # MARK: Show image
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

    # MARK: Show previous and next image
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

