from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import pytesseract
from io import BytesIO
import base64
import numpy as np
import cv2

def extract_text_from_base64(base64_string: str, original_image_path: str = "original_image.png", processed_image_path: str = "processed_image_black_bg.png") -> str:
    # Remove the prefix if present (the part before the comma)
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]

    # Fix padding
    missing_padding = len(base64_string) % 4
    if missing_padding:
        base64_string += '=' * (4 - missing_padding)

    try:
        # Decode the Base64 string into bytes
        image_data = base64.b64decode(base64_string)

        # Open the image using Pillow
        image = Image.open(BytesIO(image_data))

        # Save the original image
        image.save(original_image_path)

        # Convert to grayscale for preprocessing
        grayscale_image = image.convert("L")

        # Convert the grayscale image to a numpy array for OpenCV processing
        img_array = np.array(grayscale_image)

        # Apply Histogram Equalization
        img_eq = cv2.equalizeHist(img_array)

        # Convert back to PIL Image
        equalized_image = Image.fromarray(img_eq)

        # Sharpen the image to enhance text clarity
        enhancer = ImageEnhance.Sharpness(equalized_image)
        sharpened_image = enhancer.enhance(6.0)

        # Enhance contrast to make the text more distinct
        # Apply inversion to make the background black
        inverted_image = ImageOps.invert(sharpened_image)
        enhancer = ImageEnhance.Contrast(inverted_image)
        contrast_enhanced_image = enhancer.enhance(5)

        # Convert to numpy array for OpenCV processing
        img_array = np.array(contrast_enhanced_image)

        # Apply thresholding to ensure clear separation between text and background
        binary_image = cv2.adaptiveThreshold(img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Convert back to PIL Image for saving and OCR
        binary_image_pil = Image.fromarray(binary_image)

        # Save the processed image with black background
        binary_image_pil.save(processed_image_path)

        # OCR - Use Tesseract with `--psm 11` for sparse text
        # Include special characters in the whitelist
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()+-|\}{?/:;=<>~'
        text = pytesseract.image_to_string(binary_image_pil, config=custom_config)

        # Clean up the text (remove unwanted whitespaces)
        cleaned_text = ''.join(text.split())  # Remove unwanted spaces

        # Return the cleaned text
        return cleaned_text

    except Exception as e:
        print(f"Error occurred while processing image: {e}")
        return None
