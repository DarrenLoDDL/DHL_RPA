import os
from rembg import remove
from PIL import Image

input_directory = "input"
output_directory = "output"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through each file in the input directory
for filename in os.listdir(input_directory):
    # Check if the file is an image
    if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
        # Construct the input and output file paths
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, 'result.png')

        # Open the image
        input_image = Image.open(input_path)

        # Apply background removal using rembg library
        output_image = remove(input_image).convert("RGBA")

        # Save the processed image to the output directory
        output_image.save(output_path)
        print(f"Processed image '{filename}' saved to '{output_path}'.")

print("All images processed and saved to the 'output' directory.")