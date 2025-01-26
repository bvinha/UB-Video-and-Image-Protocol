import os
from PIL import Image, UnidentifiedImageError

def crop_center_square(image_path, size):
    try:
        img = Image.open(image_path)
    except UnidentifiedImageError:
        print(f"Cannot identify image file {image_path}. It may be corrupted.")
        return

    width, height = img.size

    if width > height:
        left = (width - size)/2
        top = (height - size)/2
        right = (width + size)/2
        bottom = (height + size)/2
    else:
        left = (width - size)/2
        top = (height - size)/2
        right = (width + size)/2
        bottom = (height + size)/2

    img_cropped = img.crop((left, top, right, bottom))
    img_cropped.save(image_path)

# Define the path to your images
image_folder = '/Users/arianmartinez/La meva unitat/asconemas_test1/'

# Get a list of all the image files in the directory
image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

# Iterate over each image file
for image_file in image_files:
    # Construct the full image path
    image_path = os.path.join(image_folder, image_file)
    # Crop the image to a centered square of 750px
    crop_center_square(image_path, 1070)