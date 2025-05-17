"""
Process for an image
"""
from typing import Optional
from PIL import Image
from PIL.ImageFile import ImageFile
from .chromatic import add_chromatic
from .noise import add_noise


def run_chromatic(
    img: Image,
    strength: float,
    blur: Optional[bool] = False
) -> Image:
    """
    Applies chromatic aberration effect to an image

    Args:
        img (Image): Source PIL image object
        strength (float): Chromatic aberration strength parameter (suggested range: 0.0-1.0)
        blur (bool, optional): Enable blur processing, defaults to False

    Returns:
        Image: Processed PIL image object

    Note:
        - Automatically adjusts image dimensions to odd numbers
        - Actual strength is input strength + 0.12
        - Applies sharpness compensation when blur is disabled
        - Uses edge detection for chromatic effect distribution
    """
    if strength <= 0:
        return

    if img.size[0] % 2 == 0 or img.size[1] % 2 == 0:
        if img.size[0] % 2 == 0:
            img = img.crop((0, 0, img.size[0] - 1, img.size[1]))
            img.load()
        if img.size[1] % 2 == 0:
            img = img.crop((0, 0, img.size[0], img.size[1] - 1))
            img.load()

    img = add_chromatic(img, strength + 0.12, not blur)
    return img


def run_noise(
    image: ImageFile,
    noise_level: Optional[float] = 0.4,
    noise_color: Optional[tuple[int, int, int]] = (255, 255, 255),
    opacity: Optional[int] = 128
) -> Image:
    """
    Applies noise effect to an image

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
    return add_noise(
        image=image,
        noise_level=noise_level,
        noise_color=noise_color,
        opacity=opacity
    )


def run(
    image: Image,
    noise_strength: float,
    noise_r: int,
    noise_g: int,
    noise_b: int,
    opacity: int,
    chromatic_strength: float,
    chromatic_blur: bool,
) -> Image:
    image = run_noise(
        image=image,
        noise_level=noise_strength,
        noise_color = (noise_r, noise_g, noise_b),
        opacity=opacity,
    )
    image = run_chromatic(
        img=image,
        strength=chromatic_strength,
        blur=chromatic_blur,
    )
    return image
