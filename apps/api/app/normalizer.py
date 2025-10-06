from __future__ import annotations
import re
from typing import Optional

WS_RE = re.compile(r"\s+")
PUNCT_SPACES_RE = re.compile(r"\s*([,:;.\-–—/()])\s*")


def _clean(s: str) -> str:
    s = s.strip()
    s = PUNCT_SPACES_RE.sub(r" \1 ", s)
    s = WS_RE.sub(" ", s)
    return s.strip()


def translate_to_en(text: str, source_lang_hint: Optional[str] = None) -> str:
    return text


def normalize_to_en(title_raw: Optional[str], desc_raw: Optional[str], lang_hint: Optional[str] = None):
    t = _clean(title_raw or "")
    d = _clean(desc_raw or "")
    t_en = translate_to_en(t, source_lang_hint=lang_hint) if t else ""
    d_en = translate_to_en(d, source_lang_hint=lang_hint) if d else ""
    title_norm = t_en[:1].upper() + t_en[1:] if t_en else None
    desc_norm = d_en or None
    return title_norm, desc_norm
