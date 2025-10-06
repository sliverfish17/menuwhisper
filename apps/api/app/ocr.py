from __future__ import annotations

from io import BytesIO
from typing import List

import pytesseract
from PIL import Image, ImageFilter, ImageOps


def ocr_lines(image_bytes: bytes, lang: str = "eng") -> List[str]:
    img = Image.open(BytesIO(image_bytes)).convert("L")

    # Enhanced preprocessing for better OCR
    if img.width < 300 or img.height < 300:
        scale_factor = max(300 / img.width, 300 / img.height)
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = img.filter(ImageFilter.SHARPEN)

    print(f"Image size: {img.size}, mode: {img.mode}")

    config = "--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,€$£¥₽₴₸₺₼₾₿₽₵₸₺₼₾₿.,-:()[]{}"

    text = pytesseract.image_to_string(img, lang=lang, config=config)
    print(f"Raw OCR text: '{text}'")

    if not text.strip():
        text = pytesseract.image_to_string(img, lang=lang)
        print(f"Raw OCR text (no config): '{text}'")

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print(f"Processed lines: {lines}")

    return lines
