
#Python indeed has powerful libraries for image processing and Optical Character Recognition (OCR), notably Pillow for image manipulation and pytesseract for OCR, which is a wrapper around Google's Tesseract-OCR Engine.

from PIL import Image, ImageFilter, ImageOps
import pytesseract
import re
import os

# Define a function to extract the date
def extract_date(text):
    date_pattern = r"\b\d{2}/\d{2}/\d{2}\b"
    date_matches = re.findall(date_pattern, text)
    return date_matches[0] if date_matches else None

# Define a function to extract the time
def extract_time(text):
    time_pattern = r"\b\d{2}:\d{2}:\d{2}\b"
    time_matches = re.findall(time_pattern, text)
    return time_matches[0] if time_matches else None

# Process an image and extract the date and time
def process_image_and_extract_datetime(image_path):
    if not os.path.exists(image_path):
        print(f"Not exist: {image_path}")
        return {"date": None, "time": None}

    try:
        image = Image.open(image_path)
        processed_image = (image
                           .crop((20, 0, 170, 90))  # Adjust crop area as needed
                           .resize((image.width * 2, image.height * 2), Image.LANCZOS)
                           .convert("L")
                           .modulate(120, 0)
                           .threshold(153)
                           .filter(ImageFilter.MedianFilter(size=3)))

        processed_image_path = f"processed_frames/{os.path.basename(image_path)}"
        processed_image.save(processed_image_path)

        text = pytesseract.image_to_string(processed_image, config='--psm 6')
        date = extract_date(text)
        time = extract_time(text)

        print(f"Processing: {image_path} | Date: {date} | Time: {time}")
        return {"date": date, "time": time}
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return {"date": None, "time": None}

# Main execution
if __name__ == "__main__":
    image_files = [f for f in os.listdir("frames") if f.endswith(('.png', '.jpg', '.jpeg'))]
    results = []

    for image_file in image_files:
        image_path = f"frames/{image_file}"
        result = process_image_and_extract_datetime(image_path)
        results.append({**result, "frame": image_file})

    # Convert results to DataFrame and save to CSV (using pandas for convenience)
    import pandas as pd
    df = pd.DataFrame(results)
    df.to_csv("updated_data.csv", index=False)
