import base64
import binascii
import io

from PIL import Image

from core.config import settings


def base64_to_bytes_image(base64_image: str) -> bytes | None:
    try:
        return base64.b64decode(str.encode(base64_image))
    except binascii.Error:
        return None


def resize_image(image: bytes) -> bytes:
    pil_image = Image.open(io.BytesIO(image))
    max_size = settings().MAX_SIZE_IMAGE

    width, height = pil_image.size
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int((new_width / width) * height)
        else:
            new_height = max_size
            new_width = int((new_height / height) * width)
        resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    else:
        resized_image = pil_image

    resized_image = resized_image.convert("RGB")
    byte_array = io.BytesIO()
    resized_image.save(byte_array, format="JPEG")

    return byte_array.getvalue()
