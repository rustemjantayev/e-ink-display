from PIL import Image, ImageOps


def convert_to_moderate_vibrant_image(input_image_path, output_image_path, target_size=(600, 448), vibrancy_factor=0.5):
    """
    Convert an image to use a strict 7-color palette with a mix of vibrant colors and gray, making the colors less intense.
    Automatically rotates the image by 90 degrees if it is in portrait orientation.
    """
    try:
        # Open the input image
        img = Image.open(input_image_path)

        # Ensure the image is in RGB mode
        img = img.convert("RGB")

        # Check if the image is in portrait orientation
        if img.height > img.width:
            img = img.rotate(90, expand=True)  # Rotate 90 degrees if in portrait orientation

        # Resize the image to target size
        img = ImageOps.pad(img, target_size, color=(255, 255, 255), method=Image.LANCZOS)


        # Define a 7-color palette (more vibrant colors)
        palette = [
            (0, 0, 0),            # Black
            (255, 255, 255),      # White
            (255, 0, 0),          # Red
            (0, 255, 0),          # Green
            (0, 0, 255),          # Blue
            (255, 255, 0),        # Yellow
            (255, 165, 0),        # Orange
        ]

        # Helper function to mix color with gray
        def mix_with_gray(color, factor):
            """
            Mix the given color with gray based on the vibrancy factor (0 to 1).
            A factor of 0 will result in pure gray, and a factor of 1 will keep the original color.
            """
            gray = (int(255 * (1 - factor)), int(255 * (1 - factor)), int(255 * (1 - factor)))
            mixed_color = (
                int(color[0] * factor + gray[0] * (1 - factor)),
                int(color[1] * factor + gray[1] * (1 - factor)),
                int(color[2] * factor + gray[2] * (1 - factor))
            )
            return mixed_color

        # Apply the mixing function to the palette
        toned_palette = []
        for color in palette:
            toned_palette.extend(mix_with_gray(color, vibrancy_factor))

        # Create a new palette image
        palette_image = Image.new("P", (1, 1))
        palette_image.putpalette(toned_palette)

        # Quantize the image with the mixed palette
        img = img.quantize(palette=palette_image, dither=Image.FLOYDSTEINBERG)

        # Save the image in BMP format (ensure compatibility with your e-ink display)
        img.save(output_image_path, format="BMP")

        print(f"Image successfully converted and saved at {output_image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_image = "images.jpeg"  # Replace with your input image file name
output_image = "output.bmp"  # Replace with your desired output BMP file name
vibrancy_factor = 0.92  # Adjust this factor to make the colors less intense (0.0 is fully gray, 1.0 is full color)


convert_to_moderate_vibrant_image(input_image, output_image, vibrancy_factor=vibrancy_factor)