import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance, ImageOps
from PIL import ImageTk
"""
@author: GoktugGulcan
"""
class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.image = None
        self.original_image = None
        self.image_path = None

        # Setup the GUI layout
        self.setup_gui()

    def setup_gui(self):
        # Layout configuration
        control_frame = tk.Frame(self.root)
        control_frame.pack(side='right', fill='y')

        image_frame = tk.Frame(self.root)
        image_frame.pack(side='left', fill='both', expand=True)

        # Buttons and sliders
        tk.Button(control_frame, text='Open Image', command=self.open_image).pack(fill='x')
        tk.Button(control_frame, text='Save Image', command=self.save_image).pack(fill='x')
        
        self.brightness_slider = tk.Scale(control_frame, from_=0.1, to=2.0, resolution=0.1, orient='horizontal', label='Brightness')
        self.brightness_slider.set(1.0)  # default value
        self.brightness_slider.pack(fill='x')
        tk.Button(control_frame, text='Apply Brightness', command=lambda: self.adjust_brightness(self.brightness_slider.get())).pack(fill='x')
        
        self.contrast_slider = tk.Scale(control_frame, from_=0.1, to=2.0, resolution=0.1, orient='horizontal', label='Contrast')
        self.contrast_slider.set(1.0)  # default value
        self.contrast_slider.pack(fill='x')
        tk.Button(control_frame, text='Apply Contrast', command=lambda: self.adjust_contrast(self.contrast_slider.get())).pack(fill='x')

        tk.Button(control_frame, text='Red Filter', command=lambda: self.apply_color_filter('red')).pack(fill='x')
        tk.Button(control_frame, text='Green Filter', command=lambda: self.apply_color_filter('green')).pack(fill='x')
        tk.Button(control_frame, text='Blue Filter', command=lambda: self.apply_color_filter('blue')).pack(fill='x')
        
        tk.Button(control_frame, text='Reset Image', command=self.reset_image).pack(fill='x')

        # Image display
        self.image_label = tk.Label(image_frame)
        self.image_label.pack(fill='both', expand=True)

    def open_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.original_image = self.image.copy()
            self.display_image()

    def save_image(self):
        if self.image:
            path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if path:
                self.image.save(path)

    def adjust_brightness(self, factor):
        self.image = ImageEnhance.Brightness(self.original_image).enhance(factor)
        self.display_image()

    def adjust_contrast(self, factor):
        self.image = ImageEnhance.Contrast(self.original_image).enhance(factor)
        self.display_image()

    def apply_color_filter(self, color):
        if self.image:
            r, g, b = self.original_image.split()
            if color == 'red':
                self.image = Image.merge("RGB", (r, b.point(lambda p: 0), g.point(lambda p: 0)))
            elif color == 'green':
                self.image = Image.merge("RGB", (r.point(lambda p: 0), g, b.point(lambda p: 0)))
            elif color == 'blue':
                self.image = Image.merge("RGB", (r.point(lambda p: 0), g.point(lambda p: 0), b))
            self.display_image()

    def reset_image(self):
        if self.original_image:
            self.image = self.original_image.copy()
            self.brightness_slider.set(1.0)
            self.contrast_slider.set(1.0)
            self.display_image()

    def display_image(self):
        max_size = 600, 400
        img_copy = self.image.copy()
        img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(img_copy)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

# Create the main window and pass it to the ImageEditor class
root = tk.Tk()
app = ImageEditor(root)
root.mainloop()
