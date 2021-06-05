from tkinter import Toplevel, Label, Scale, Button, HORIZONTAL, RIGHT
from tkinter.constants import LEFT
from createCartoon import createCartoon
import cv2


class AdjustFrame(Toplevel):

    def __init__(self, master=None, data=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.processing_image = self.master.processed_image

        self.adjustFrameData = data

        self.line_size = data['line_size']
        self.previous_line_size = data['line_size']

        self.blur_value = data['blur_value']
        self.previous_blur_value = data['blur_value']

        self.total_color = data['total_color']
        self.previous_total_color = data['total_color']

        self.pixel_dia = data['pixel_dia']
        self.previous_pixel_dia = data['pixel_dia']

        self.sigma_space = data['sigma_space']
        self.previous_sigma_space = data['sigma_space']

        self.sigma_color = data['sigma_color']
        self.previous_sigma_color = data['sigma_color']
        
        self.apply_button = Button(self, text="Apply")
        self.preview_button = Button(self, text="Preview")
        self.cancel_button = Button(self, text="Cancel")

        def fix_line(n):
            n = int(n)
            if not n % 2:
                self.line_size_scale.set(n+1)

        self.line_size_label = Label(self, text="Line Size")
        self.line_size_scale = Scale(self, from_=3, to_=15, length=250, command=fix_line,
                                      orient=HORIZONTAL)
        self.line_size_scale.set(self.line_size)

        def fix_blur(n):
            n = int(n)
            if not n % 2:
                self.blur_value_scale.set(n+1)

        self.blur_value_label = Label(self, text="Blur Value")
        self.blur_value_scale = Scale(self, from_=3, to_=15, length=250, command=fix_blur,
                                      orient=HORIZONTAL)
        self.blur_value_scale.set(self.blur_value)

        self.total_color_label = Label(self, text="Total Colour")
        self.total_color_scale = Scale(self, from_=5, to_=12, length=250, resolution=1,
                                      orient=HORIZONTAL)
        self.total_color_scale.set(self.total_color)

        self.pixel_dia_label = Label(self, text="Pixel Diameter")
        self.pixel_dia_scale = Scale(self, from_=2, to_=15, length=250, resolution=1,
                                      orient=HORIZONTAL)
        self.pixel_dia_scale.set(self.pixel_dia)

        self.sigma_color_label = Label(self, text="Sigma Color")
        self.sigma_color_scale = Scale(self, from_=100, to_=300, length=250, resolution=1,
                                      orient=HORIZONTAL)
        self.sigma_color_scale.set(self.sigma_color)

        self.sigma_space_label = Label(self, text="Sigma Space")
        self.sigma_space_scale = Scale(self, from_=100, to_=300, length=250, resolution=1,
                                      orient=HORIZONTAL)
        self.sigma_space_scale.set(self.sigma_space)

        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.preview_button.bind("<ButtonRelease>", self.show_button_release)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.line_size_label.pack()
        self.line_size_scale.pack()
        self.blur_value_label.pack()
        self.blur_value_scale.pack()
        self.total_color_label.pack()
        self.total_color_scale.pack()
        self.pixel_dia_label.pack()
        self.pixel_dia_scale.pack()
        self.sigma_color_label.pack()
        self.sigma_color_scale.pack()
        self.sigma_space_label.pack()
        self.sigma_space_scale.pack()
        self.cancel_button.pack(side=RIGHT)
        self.preview_button.pack(side=LEFT)
        self.apply_button.pack(side=LEFT)

    def apply_button_released(self, event):
        self.master.processed_image = self.processing_image
        self.close()

    def show_button_release(self, event):
        self.adjustFrameData = {
            "line_size": self.line_size_scale.get(),
            "blur_value": self.blur_value_scale.get(),
            "total_color": self.total_color_scale.get(),
            "pixel_dia": self.pixel_dia_scale.get(),
            "sigma_space": self.sigma_space_scale.get(),
            "sigma_color": self.sigma_color_scale.get(),
        }

        self.line_size = self.adjustFrameData['line_size']
        self.blur_value = self.adjustFrameData['blur_value']
        self.total_color = self.adjustFrameData['total_color']
        self.pixel_dia = self.adjustFrameData['pixel_dia']
        self.sigma_space = self.adjustFrameData['sigma_space']
        self.sigma_color = self.adjustFrameData['sigma_color']

        cartoon_maker = createCartoon(self.original_image, self.adjustFrameData)
        self.processing_image = cartoon_maker.get_cartoon()
        self.show_image(self.processing_image)

    def cancel_button_released(self, event):
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def close(self):
        self.show_image()
        self.destroy()