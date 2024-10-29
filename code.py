import fitz
import os
from PIL import Image
import io

file = '/content/CV.pdf'
pdf_file = fitz.open(file)

# Get the base name of the file without the extension
base_name = os.path.splitext(os.path.basename(file))[0]

# Initialize variables to keep track of the largest image
max_size = 0
largest_image = None

# Loop through each page in the PDF
for page_num in range(pdf_file.page_count):
    page = pdf_file[page_num]
    images = page.get_images(full=True)
    
    # Loop through each image in the page
    for img in images:
        xref = img[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        
        # Check image size
        image_size = len(image_bytes)
        
        # Update largest image if the current one is bigger
        if image_size > max_size:
            max_size = image_size
            largest_image = image_bytes

# Save the largest image if it exists
if largest_image:
    # Convert bytes to a PIL image
    pil_image = Image.open(io.BytesIO(largest_image))
    
    # Define image path with just the PDF base name
    image_path = f"{base_name}.png"
    
    # Save the image
    pil_image.save(image_path)
    print(f"Saved the largest image to {image_path}")
else:
    print("No images found in the PDF.")
