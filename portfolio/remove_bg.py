from rembg import remove
from PIL import Image

input_path = 'assets/raw_profile.jpg'
output_path = 'assets/profile.png'

# Processing the image
input = Image.open(input_path)

# Removing the background
output = remove(input)

# Saving the image
output.save(output_path)
print("Background removed successfully!")
