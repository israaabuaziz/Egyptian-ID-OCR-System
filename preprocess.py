import cv2
import numpy as np
import cv2

def resize(image, flag):
    if image is None:
        raise ValueError("Input image is None or invalid.")
    resize_config = {
        "id": (650, 800),  # ID card size
        "location": (750, 400),  # Location field size
        "firstname": (700, 300),  # First name field size
        "secondname": (500, 200),  # Second name field size
        "default": (image.shape[1], image.shape[0])  # Default: keep original size
    }

    target_width, target_height = resize_config.get(flag, resize_config["default"])

    if flag != "default":
        input_height, input_width = image.shape[:2]
        input_aspect_ratio = input_width / input_height

        target_aspect_ratio = target_width / target_height

        if input_aspect_ratio > target_aspect_ratio:
            new_width = target_width
            new_height = int(target_width / input_aspect_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * input_aspect_ratio)

        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    else:
        resized_image = image

    return resized_image
def preprocess_image(image, flag):
    resized_image = resize(image , flag)
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, thresh = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Binarize
    
    return thresh
