"""
Process for an image
"""
from typing import Optional
import numpy as np
from PIL import Image
from PIL.ImageFile import ImageFile
from .chromatic import add_chromatic
from .noise import add_noise
from .glow import add_glow


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
        - Automatically adjusts image dimensions to odd numbers during processing,
          then restores the original size by repeating edge pixels
        - Actual strength is input strength + 0.12
        - Applies sharpness compensation when blur is disabled
        - Uses edge detection for chromatic effect distribution
    """
    if strength <= 0:
        return img

    size = img.size
    if img.size[0] % 2 == 0 or img.size[1] % 2 == 0:
        if img.size[0] % 2 == 0:
            img = img.crop((0, 0, img.size[0] - 1, img.size[1]))
            img.load()
        if img.size[1] % 2 == 0:
            img = img.crop((0, 0, img.size[0], img.size[1] - 1))
            img.load()

    img = add_chromatic(img, strength + 0.12, not blur)
    if img.size != size:
        data = np.asarray(img)
        pad = ((0, size[1] - img.size[1]), (0, size[0] - img.size[0]), (0, 0))
        img = Image.fromarray(np.pad(data, pad, mode="edge"), img.mode)
    return img


def run_noise(
    image: ImageFile,
    noise_level: Optional[float] = 0.4,
    noise_color: Optional[tuple[int, int, int]] = (255, 255, 255),
    opacity: Optional[int] = 128,
    offset_percentage: Optional[int] = 20,
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
        offset_percentage (int): Percentage range for offset (0-100) (default: 20)

    Returns:
        Image: New Image object with noise layer composited
    """
    return add_noise(
        image=image,
        noise_level=noise_level,
        noise_color=noise_color,
        opacity=opacity,
        offset_percentage=offset_percentage,
    )


def run_glow(
    image: ImageFile,
    strength: Optional[float] = 0.6,
    threshold: Optional[float] = 0.6,
    radius: Optional[float] = 3,
    color: Optional[tuple[int, int, int]] = (255, 240, 220),
    soft_focus: Optional[float] = 0.3,
    edge_softness: Optional[float] = 0.2,
) -> Image:
    """
    Applies soft glow effect (ambient glow / soft focus / edge haze) to an image

    Args:
        image (ImageFile): Source PIL Image object
        strength (float, optional): Glow strength [0-2.0], 0 = disabled (default: 0.6)
        threshold (float, optional): Luminance threshold of highlights that glow [0-1.0] (default: 0.6)
        radius (float, optional): Glow radius as percentage of the image short side (default: 3)
        color (tuple[int, int, int], optional): RGB tint of the glow (default: (255, 240, 220))
        soft_focus (float, optional): Opacity of the soft focus layer [0-1.0] (default: 0.3)
        edge_softness (float, optional): Strength of haze on image edges [0-1.0] (default: 0.2)

    Returns:
        Image: Processed PIL image object
    """
    if strength <= 0:
        return image

    return add_glow(
        image=image,
        strength=strength,
        threshold=threshold,
        radius=radius,
        color=color,
        soft_focus=soft_focus,
        edge_softness=edge_softness,
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
    offset_percentage: int,
    glow_strength: float = 0,
    glow_threshold: float = 0.6,
    glow_radius: float = 3,
    glow_r: int = 255,
    glow_g: int = 240,
    glow_b: int = 220,
    glow_soft_focus: float = 0.3,
    glow_edge_softness: float = 0.2,
) -> Image:
    image = run_glow(
        image=image,
        strength=glow_strength,
        threshold=glow_threshold,
        radius=glow_radius,
        color=(glow_r, glow_g, glow_b),
        soft_focus=glow_soft_focus,
        edge_softness=glow_edge_softness,
    )
    image = run_noise(
        image=image,
        noise_level=noise_strength,
        noise_color = (noise_r, noise_g, noise_b),
        opacity=opacity,
        offset_percentage=offset_percentage,
    )
    image = run_chromatic(
        img=image,
        strength=chromatic_strength,
        blur=chromatic_blur,
    )
    return image
