import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Uploader")

        # Create a label to display the uploaded image
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Create a button to trigger image upload
        upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        upload_button.pack(pady=10)

    def upload_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            # Display the selected image
            self.display_image(file_path)

    def display_image(self, file_path):
        # Open and resize the image
        image = Image.open(file_path)
        image = image.resize((300, 300), Image.ANTIALIAS)

        # Convert the image to Tkinter PhotoImage
        photo = ImageTk.PhotoImage(image)

        # Update the label with the new image
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference to avoid garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUploader(root)
    root.mainloop()
