"""
Add noise to image
"""
import random
from typing import Optional
from PIL import Image
from PIL.ImageFile import ImageFile


def add_noise(
    image: ImageFile,
    noise_level: Optional[float] = 0.4,
    noise_color: Optional[tuple[int, int, int]] = (255, 255, 255),
    opacity: Optional[int] = 128,
    offset_percentage: int = 20,
) -> Image:
    """
    Adds configurable noise layer to image with specified parameters

    Args:
        image (ImageFile): Source PIL Image object (RGBA mode recommended)
        noise_level (float, optional): Noise density [0-1.0]
            0.0 = no noise, 1.0 = full coverage (default: 0.1)
        noise_color (tuple[int, int, int], optional): RGB noise color 
            (default: white (255,255,255))
        opacity (int, optional): Noise opacity [0-255]
            0 = fully transparent, 255 = fully opaque (default: 128)

    Returns:
        Image: New Image object with noise layer composited
    """
    base_img = image.convert("RGBA")
    width, height = base_img.size

    noise_layer = Image.new("RGBA", (width, height))
    noise_pixels = noise_layer.load()

    for x in range(width):
        for y in range(height):
            if random.random() < noise_level:
                offset_noise_color = offset_rgb_value(*noise_color, offset_percentage=offset_percentage)
                noise_pixels[x, y] = offset_noise_color + (opacity,)

    combined = Image.alpha_composite(base_img, noise_layer)
    return combined


def offset_rgb_value(
    r: int,
    g: int,
    b: int,
    offset_percentage: int = 20,
) -> tuple[int, int, int]:
    """
    Offset RGB values with random offsets controlled by percentage range

    Args:
        r (int): Original R values (0-255)
        g (int): Original G values (0-255)
        b (int): Original B values (0-255)
        offset_percentage (int): Percentage range for offset (0-100)

    Returns:
        tuple[int,int,int]: Tuple of offset RGB values
    """

    def clamp(value):
        """Clamp value to 0-255 range"""
        return max(0, min(255, value))

    # Calculate maximum offset
    max_offset = int(255 * (offset_percentage / 100))

    # Generate random offsets for each color channel
    r_offset = random.randint(-max_offset, max_offset)
    g_offset = random.randint(-max_offset, max_offset)
    b_offset = random.randint(-max_offset, max_offset)

    # Apply offsets and ensure values are within valid range
    new_r = clamp(r + r_offset)
    new_g = clamp(g + g_offset)
    new_b = clamp(b + b_offset)

    return (new_r, new_g, new_b)