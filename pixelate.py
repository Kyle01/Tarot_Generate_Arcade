import os
import math
from PIL import Image

# -------------------------
# 1) Define your color palette (RGB)
# -------------------------
CUSTOM_PALETTE = [
    (43, 15, 84),
    (171, 31, 101),
    (255, 79, 105),
    (255, 247, 248),
    (255, 129, 66),
    (255, 218, 69),
    (51, 104, 220),
    (73, 231, 236),
]

# Block size 25 => scale factor = 0.25
BLOCK_SIZE = 30
SCALE_FACTOR = BLOCK_SIZE * 0.01  # = 0.25

# -------------------------
# 2) Folders
# -------------------------
# Edit SOURCE_FOLDER if needed:
SOURCE_FOLDER = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "brain",
    "projects",
    "Tarot_generate_Arcade",
    "assets"
)
OUTPUT_FOLDER = os.path.join(SOURCE_FOLDER, "convertedx2")

# Create the output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def pixelate_and_convert(img_path, scale, palette):
    """
    1) Opens the image,
    2) Pixelates it by resizing down and up using Nearest Neighbor,
    3) Converts each pixel to the nearest color in `palette`,
    4) Returns the resulting Pillow Image.
    """
    # Open the image with Pillow
    with Image.open(img_path) as img:
        # Convert to RGBA or RGB to ensure we can work with color data
        img = img.convert("RGB")
        width, height = img.size

        # 1) Scale down
        new_w = max(1, int(width * scale))
        new_h = max(1, int(height * scale))

        # Resize down (pixelation step) using NEAREST
        img_small = img.resize((new_w, new_h), Image.Resampling.NEAREST)

        # 2) Scale back up to original size
        img_pixelated = img_small.resize((width, height), Image.Resampling.NEAREST)

        # 3) Map each pixel to the nearest color in the palette
        # Load pixel data
        pixels = img_pixelated.load()
        for y in range(height):
            for x in range(width):
                # Current pixel color
                r, g, b = pixels[x, y]
                # Find nearest palette color
                r_new, g_new, b_new = nearest_palette_color(r, g, b, palette)
                # Replace with that color
                pixels[x, y] = (r_new, g_new, b_new)

        return img_pixelated


def nearest_palette_color(r, g, b, palette):
    """Given an (r, g, b) color, return the closest color in the palette."""
    best_dist = math.inf
    best_color = (r, g, b)

    for (pr, pg, pb) in palette:
        dist = color_distance(r, g, b, pr, pg, pb)
        if dist < best_dist:
            best_dist = dist
            best_color = (pr, pg, pb)
    return best_color


def color_distance(r1, g1, b1, r2, g2, b2):
    """Euclidean distance between two RGB colors."""
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


def main():
    # List all files in SOURCE_FOLDER
    all_files = os.listdir(SOURCE_FOLDER)

    # Filter for images only (png, jpg, jpeg, etc.)
    valid_exts = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")
    image_files = [f for f in all_files if f.lower().endswith(valid_exts)]

    for file_name in image_files:
        in_path = os.path.join(SOURCE_FOLDER, file_name)

        print(f"Processing: {file_name}")

        # Pixelate and color-convert
        out_img = pixelate_and_convert(in_path, SCALE_FACTOR, CUSTOM_PALETTE)

        # Build output path (switch extension to .png)
        base_name, _ = os.path.splitext(file_name)
        out_name = f"{base_name}.png"
        out_path = os.path.join(OUTPUT_FOLDER, out_name)

        # Save
        out_img.save(out_path, format="PNG")

        print(f"  Saved => {out_path}")


if __name__ == "__main__":
    main()
    print("\nAll done!")
