import cv2
import numpy as np

input_path = 'assets/raw_profile.jpg'
output_path = 'assets/profile.png'

img = cv2.imread(input_path)
if img is None:
    print("Could not read image")
    exit(1)

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Find blue color
lower_blue = np.array([90, 40, 40])
upper_blue = np.array([140, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Invert mask (so foreground is white)
mask = cv2.bitwise_not(mask)

# Find the largest contour (the person) and create a fresh mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
fresh_mask = np.zeros_like(mask)
if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    cv2.drawContours(fresh_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

# Feather/smooth the edge of the mask
fresh_mask = cv2.GaussianBlur(fresh_mask, (11, 11), 0)

# Apply alpha mask
b, g, r = cv2.split(img)
dst = cv2.merge((b, g, r, fresh_mask))

cv2.imwrite(output_path, dst)
print("Smooth background removal complete.")
