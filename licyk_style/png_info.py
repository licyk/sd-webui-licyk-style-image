"""
Image process
"""
from typing import Optional
from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from PIL.ImageFile import ImageFile


def get_image_info(
    image: ImageFile,
) -> dict:
    """
    Get png info from image object
    Args:
        image (ImageFile): PIL Image object containing file format metadata
            (typically from PNG/TIFF/JPG files)

    Returns:
        dict: Metadata dictionary containing format-specific information
            - For PNG: Includes tEXt chunks like 'Parameters', 'Software'
            - For JPEG: May contain EXIF data when available
            - Empty dict for unsupported formats
    """
    return image.info


def open_image(image_path: str | Path) -> ImageFile:
    """
    Opens an image file using PIL.Image.open with path validation

    Args:
        image_path (str | Path): File path to the image
            Supports common formats: PNG/JPEG/GIF/BMP

    Returns:
        ImageFile: PIL Image object in read mode
            Note: Returned image requires explicit close() 
            or use with context manager
    """
    return Image.open(image_path)


def save_image(
    image: ImageFile,
    output_path: str | Path,
    png_info: Optional[dict] = None
) -> None:
    """
    Saves a PIL Image object to the specified path with optional PNG metadata.

    Args:
        image (Image): PIL Image object to be saved
        output_path (str | Path): Destination path for the image file. Must have .png extension
        png_info (Optional[dict]): Dictionary containing PNG metadata key-value pairs

    Raises:
        ValueError: If output_path does not have .png extension
        IOError: If image writing operation fails
    """
    metadata = PngInfo()
    if png_info is not None:
        for key, value in png_info.items():
            metadata.add_text(
                key=key,
                value=value
            )

    image.save(output_path, pnginfo=metadata)
