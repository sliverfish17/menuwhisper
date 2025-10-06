from __future__ import annotations

import re

from app.db import get_db
from app.models import MenuItem, Restaurant
from app.normalizer import normalize_to_en
from app.ocr import ocr_lines
from app.services import upsert_embeddings_for_restaurant
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

router = APIRouter(prefix="/ingest", tags=["ingest"])

PRICE_RE = re.compile(
    r"(?P<price>\d+[.,]?\d*)\s*(?P<cur>pln|uah|usd|eur|€|zł|zl)?", re.I
)
ALPHA_RE = re.compile(r"[A-Za-zА-Яа-яЁёІіЇїЄє]")


def parse_menu_lines(lines: list[str], default_currency: str = "PLN"):
    items = []
    for ln in lines:
        s = re.sub(r"\s+", " ", ln).strip()

        if len(s) < 5:
            continue
        if not ALPHA_RE.search(s):
            continue
        if s.endswith(":") or s.count(" . ") > 1 or s.count(". ") > 3:
            continue

        m = PRICE_RE.search(s)
        if not m:
            items.append(
                {
                    "title": s,
                    "desc": None,
                    "price_cents": None,
                    "currency": default_currency,
                }
            )
            continue

        price_str = m.group("price").replace(",", ".")
        cur = (
            (m.group("cur") or default_currency)
            .upper()
            .replace("ZŁ", "PLN")
            .replace("ZL", "PLN")
            .replace("€", "EUR")
        )
        try:
            cents = int(round(float(price_str) * 100))
        except ValueError:
            cents = None

        title = s[: m.start()].strip(" -·—:.")
        desc = s[m.end() :].strip(" -·—:.") or None
        title = title or s
        items.append(
            {"title": title, "desc": desc, "price_cents": cents, "currency": cur}
        )
    return items


@router.post("/menu")
async def ingest_menu(
    image: UploadFile = File(...),
    restaurant_name: str = Form("Untitled"),
    currency: str = Form("PLN"),
    lang: str = Form("eng"),
    db: Session = Depends(get_db),
):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(400, detail="image_required")

    raw = await image.read()
    lines = ocr_lines(raw, lang=lang)

    # save restaurant + items
    rest = Restaurant(name=restaurant_name, name_raw=restaurant_name)
    db.add(rest)
    db.flush()

    parsed = parse_menu_lines(lines, default_currency=currency)
    for it in parsed:
        title_norm, desc_norm = normalize_to_en(it["title"], it["desc"], lang_hint=lang)
        db.add(
            MenuItem(
                restaurant_id=rest.id,
                title=it["title"] or "Untitled Item",
                title_raw=it["title"],
                description_raw=it["desc"],
                title_norm=title_norm,
                description_norm=desc_norm,
                price_cents=it["price_cents"] or 0,
                currency=it["currency"],
            )
        )
    db.commit()

    # build embeddings
    embedded = upsert_embeddings_for_restaurant(db, rest.id)

    return {
        "restaurant_id": str(rest.id),
        "lines": len(lines),
        "items_saved": len(parsed),
        "embedded": embedded,
        "preview": parsed[:5],
    }
