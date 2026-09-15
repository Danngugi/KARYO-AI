import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def load_image(path: str) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if image.width < 64 or image.height < 64:
        raise ValueError("Image is too small for chromosome analysis (minimum 64×64 pixels).")
    return image

def detect_modality(image: Image.Image) -> str:
    a = np.asarray(image, dtype=float)
    channel_spread = np.mean(np.max(a, axis=2) - np.min(a, axis=2))
    return "fluorescent" if channel_spread > 35 and np.mean(a) < 180 else "giemsa"

def prepare(image: Image.Image, modality: str) -> tuple[Image.Image, np.ndarray]:
    gray = image.convert("L")
    gray = ImageEnhance.Contrast(gray).enhance(1.8)
    gray = gray.filter(ImageFilter.MedianFilter(3))
    array = np.asarray(gray, dtype=np.uint8)
    if modality == "fluorescent":
        # Bright chromosome bodies on dark field.
        mask = array > max(25, int(np.percentile(array, 75)))
    else:
        # Dark Giemsa bodies on pale background.
        mask = array < min(220, int(np.percentile(array, 35)))
    return gray, mask

def image_qc(image: Image.Image) -> dict:
    a = np.asarray(image.convert("L"), dtype=float)
    focus = float(np.var(np.diff(a, axis=0)) + np.var(np.diff(a, axis=1)))
    return {"width_px": image.width, "height_px": image.height, "contrast_sd": round(float(a.std()), 2),
            "focus_proxy": round(focus, 2), "adequate": bool(a.std() >= 12 and focus >= 20)}
