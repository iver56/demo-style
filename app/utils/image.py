"""Various image utils."""

import base64
import os

import six
from PIL import Image


def pil_image_to_base64(image):
    """Convert a Pillow Image instance to a base64 string."""

    if not image:
        return None

    image_buffer = six.BytesIO()
    image.save(image_buffer, format="PNG")
    return base64.b64encode(image_buffer.getvalue()).decode("utf-8")


def base64_png_image_to_pillow_image(base64_string):
    """Convert a base64 string (that represents a PNG image) to a Pillow Image instance."""
    img_data = base64.b64decode(str(base64_string))  # Decode base64
    image = Image.open(six.BytesIO(img_data))  # Decode the PNG data
    return image


def get_image_file_paths(image_root_path):
    """Return a list of paths to all image files in a directory (does not check subdirectories)."""
    image_file_paths = []

    for root, dirs, filenames in os.walk(image_root_path):
        filenames = sorted(filenames)
        for filename in filenames:
            input_path = os.path.abspath(root)
            file_path = os.path.join(input_path, filename)

            file_extension = filename.split(".")[-1]
            if (
                file_extension.lower() in ("png", "jpg", "jpeg")
                and ".__label__." not in filename
            ):
                image_file_paths.append(file_path)

        break  # prevent descending into subfolders

    return image_file_paths
