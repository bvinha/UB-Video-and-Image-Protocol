import os
import re
from PIL import Image
import pytesseract

# Set the directory containing the images
dir2 = "/Volumes/OASIS ROV/videos/VIDEOS TRAINING/Frames2/selected2"

# List all image files in the directory
files2 = [os.path.join(dir2, f) for f in os.listdir(dir2) if f.endswith('.tiff')]

# Initialize an empty dictionary to store extracted time information
time_info_dict = {}

def extract_time_from_line(line):
    time_pattern = r"\b\d{1,2}(:\d{2})?\s*(AM|PM|am|pm)?\b"
    times = re.findall(time_pattern, line, re.IGNORECASE)
    return times

# Function to process an image and extract time information
def process_image(image_path):
    image = Image.open(image_path)
    # Image preprocessing steps here

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)
    extracted_text = str(text)

    # Extracted time information from the second line
    lines = extracted_text.split("\n")
    if len(lines) >= 2:
        second_line = lines[1]
        extracted_time = extract_time_from_line(second_line)
        return extracted_time
    else:
        return None

# Iterate through image files and process each image
for image_file in files2:
    extracted_time = process_image(image_file)  # image_file is passed as an argument
    if extracted_time is not None:
        time_info_dict[image_file] = extracted_time

print(time_info_dict)
