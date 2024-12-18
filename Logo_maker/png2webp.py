import os
from PIL import Image

# Set input and output directories
input_directory = "input"
output_directory = "output"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through each file in the input directory
for filename in os.listdir(input_directory):
    # Check if the file is a PNG image
    if filename.lower().endswith(".png"):
        # Construct the input and output file paths
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".webp")

        # Open the PNG image
        png_image = Image.open(input_path)

        # Convert the image to WebP format
        png_image.save(output_path, "WEBP")

        print(f"PNG image '{filename}' converted to WebP format.")

print("All PNG images converted to WebP format and saved in the 'output' directory.")