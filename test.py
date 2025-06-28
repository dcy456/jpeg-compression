import os
from PIL import Image
import numpy as np

input_dir = "./img"
output_dir = "./img_jpeg"
os.makedirs(output_dir, exist_ok=True)

def count_unchanged_pixels(original, compressed):
    unchanged = original == compressed
    count_per_channel = np.sum(unchanged, axis=(0, 1))
    return count_per_channel

for filename in os.listdir(input_dir):
    if not filename.lower().endswith(('.png', '.bmp', '.tiff', '.jpeg', '.jpg', '.webp')):
        continue

    original_path = os.path.join(input_dir, filename)
    with Image.open(original_path) as img:
        img = img.convert('RGB')
        img_np = np.array(img)

        jpeg_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".jpg")
        img.save(jpeg_path, format="JPEG", quality=30)  

        with Image.open(jpeg_path) as jpeg_img:
            jpeg_img = jpeg_img.convert('RGB')
            jpeg_np = np.array(jpeg_img)

        if img_np.shape != jpeg_np.shape:
            print(f"skip {filename}")
            continue

        total_pixels = img_np.shape[0] * img_np.shape[1]
        unchanged_counts = count_unchanged_pixels(img_np, jpeg_np)
        ratios = unchanged_counts / total_pixels * 100

        print(f"image: {filename}; amount of pixels:{total_pixels}")
        print(f"  unchanged pixels in R channel: {unchanged_counts[0]} ({ratios[0]:.2f}%)")
        print(f"  unchanged pixels in R channel:{unchanged_counts[1]} ({ratios[1]:.2f}%)")
        print(f"  unchanged pixels in B channel: {unchanged_counts[2]} ({ratios[2]:.2f}%)")
        # print(f"{unchanged_counts[0]}")
        # print(f"{unchanged_counts[1]}")
        # print(f"{unchanged_counts[2]}")
        # print(f"{ratios[0]:.2f}%")
        # print(f"{ratios[1]:.2f}%")
        # print(f"{ratios[2]:.2f}%")
        print("")

print("Finish")
