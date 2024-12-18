import pygame
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
    if filename.lower().endswith(".svg"):
        # Construct the input and output file paths
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".png")

        # Convert the image to png format
        surface = pygame.image.load(input_path)
        pygame.image.save(surface, filename+".png")

        print(f"PNG image '{filename}' converted to PNG format.")

print("All SVG images converted to PNG format and saved in the 'output' directory.")

