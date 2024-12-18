import os
from PIL import Image

def resize_image(image, max_width, max_height):
    width, height = image.size

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Calculate the new dimensions while maintaining the aspect ratio
    if aspect_ratio > max_width / max_height:
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    return resized_image

# Set input and output directories
input_directory = "input"
output_directory = "output"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through each file in the input directory
for filename in os.listdir(input_directory):
    # Check if the file is an image
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        # Construct the input and output file paths
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename)

        # Open the image
        image = Image.open(input_path)

        # Resize the image
        resized_image = resize_image(image, 70, 50)

        # Save the resized image
        resized_image.save(output_path)

        print(f"Image '{filename}' resized and saved as '{output_path}'.")

print("All images resized and saved in the 'output' directory.")