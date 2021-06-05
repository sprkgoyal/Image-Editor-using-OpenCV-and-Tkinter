from cv2 import cv2
import numpy as np

class createCartoon:
    def __init__(self, image = None, data = None):
        if data is not None:
            self.line_size = data['line_size']
            self.blur_value = data['blur_value']
            self.total_color = data['total_color']
            self.pixel_dia = data['pixel_dia']
            self.sigma_space = data['sigma_space']
            self.sigma_color = data['sigma_color']
        self.image = image

    def get_cartoon(self, image = None, values = None):

        if image is not None:
            self.image = image

        if values is not None:
            self.line_size = values['line_size']
            self.blur_value = values['blur_value']
            self.total_color = values['total_color']
            self.pixel_dia = values['pixel_dia']
            self.sigma_space = values['sigma_space']
            self.sigma_color = values['sigma_color']
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, self.blur_value)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, self.line_size, self.blur_value)

        data = np.float32(self.image).reshape((-1, 3))

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

        ret, label, center = cv2.kmeans(data, self.total_color, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(self.image.shape)

        blurred = cv2.bilateralFilter(result, d=7, sigmaColor=self.sigma_color, sigmaSpace=self.sigma_space)
        cartoon = cv2.bitwise_or(blurred, blurred, mask=edges)

        return cartoon