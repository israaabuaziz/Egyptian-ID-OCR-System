import cv2
import numpy as np



# def resize(image, flag):
#     sizes = {
#         "id": (650, 800),
#         "location": (750, 400),
#         "firstname": (200, 200),
#         "secondname": (500, 200),
#     }
#     return cv2.resize(image, sizes.get(flag, image.shape[:2]), interpolation=cv2.INTER_LINEAR)


# # Preprocessing function
# def preprocess_image(image, flag):
#     resized_image = resize(image , flag)
#     gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
#     # gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)  # Resize to enhance small text
#     # blurred = cv2.GaussianBlur(gray, (3, 3), 0)  # Reduce noise
#     _, thresh = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Binarize

#     return thresh

import cv2

def resize(image, flag):
    # sourcery skip: lift-return-into-if, remove-unnecessary-else, swap-if-else-branches
    # Check if the input image is valid
    if image is None:
        raise ValueError("Input image is None or invalid.")

    # Define target dimensions for each flag
    resize_config = {
        "id": (650, 800),  # ID card size
        "location": (750, 400),  # Location field size
        "firstname": (700, 300),  # First name field size
        "secondname": (500, 200),  # Second name field size
        "default": (image.shape[1], image.shape[0])  # Default: keep original size
    }

    # Get target dimensions based on flag
    target_width, target_height = resize_config.get(flag, resize_config["default"])

    # Resize the image while maintaining aspect ratio
    if flag != "default":
        # Calculate the aspect ratio of the input image
        input_height, input_width = image.shape[:2]
        input_aspect_ratio = input_width / input_height

        # Calculate the aspect ratio of the target dimensions
        target_aspect_ratio = target_width / target_height

        # Adjust dimensions to maintain aspect ratio
        if input_aspect_ratio > target_aspect_ratio:
            # Fit to width
            new_width = target_width
            new_height = int(target_width / input_aspect_ratio)
        else:
            # Fit to height
            new_height = target_height
            new_width = int(target_height * input_aspect_ratio)

        # Resize the image
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    else:
        # Keep the original size
        resized_image = image

    return resized_image

# Resize function
# def resize(image, flag):
#     if flag == "id":
#         return cv2.resize(image, (650, 800))
#     elif flag == 1:
#         return cv2.resize(image, (750, 750), interpolation=cv2.INTER_LINEAR)
#     elif flag == "firstname":
#         return cv2.resize(image, (700, 300))
#     elif flag == "secondname":
#         return cv2.resize(image, (500, 200))
#     else:
#         return image
# Preprocessing function
def preprocess_image(image, flag):
    resized_image = resize(image , flag)
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, thresh = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Binarize
    
    return thresh
