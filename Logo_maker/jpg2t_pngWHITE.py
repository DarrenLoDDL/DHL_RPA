import os
from PIL import Image, ImageEnhance

def sharpen_white_background(image_path, output_path):
    # Open the image
    image = Image.open(image_path)

    # Enhance the image to sharpen the white areas
    enhancer = ImageEnhance.Sharpness(image)
    sharpened_image = enhancer.enhance(2.0)

    # Convert the image to RGBA mode
    sharpened_image = sharpened_image.convert("RGBA")

    # Get the pixel data of the image
    data = sharpened_image.getdata()

    # Create a new image with transparent background
    transparent_image = []
    for pixel in data:
        # Check if the pixel is white
        if pixel[:3] == (255, 255, 255):
            # Set the pixel as transparent
            transparent_image.append((255, 255, 255, 0))
        else:
            # Keep the original pixel
            transparent_image.append(pixel)

    # Create a new image with the transparent background
    new_image = Image.new("RGBA", sharpened_image.size)
    new_image.putdata(transparent_image)

    # Save the image with sharpened white areas and removed white background
    new_image.save(output_path).convert("RGBA")

    print(f"Image with sharpened white areas and white background removed saved as '{output_path}'.")

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

        # Call the function to sharpen white areas and remove white background
        sharpen_white_background(input_path, output_path)

print("All images processed and saved in the 'output' directory.")