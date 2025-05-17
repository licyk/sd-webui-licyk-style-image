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
    opacity: Optional[int] = 128
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
                noise_pixels[x, y] = noise_color + (opacity,)

    combined = Image.alpha_composite(base_img, noise_layer)
    return combined
