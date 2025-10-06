from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..db import get_db
from ..models import Restaurant, MenuItem
from sqlalchemy.orm import Session

router = APIRouter(prefix="/menu", tags=["menu"])


class MenuItemRequest(BaseModel):
    title: str
    desc: str
    price_cents: int
    currency: str


class SeedRequest(BaseModel):
    restaurant_name: str
    items: List[MenuItemRequest]


@router.post("/seed")
async def seed_restaurant(body: SeedRequest):
    """Seed a restaurant with menu items"""
    db = next(get_db())

    try:
        # Create restaurant
        rest = Restaurant(
            name=body.restaurant_name,
            name_raw=body.restaurant_name,
        )
        db.add(rest)
        db.flush()  # Get the ID without committing

        # Create menu items
        for it in body.items:
            item = MenuItem(
                restaurant_id=rest.id,
                title=it.title,
                title_raw=it.title,
                description_raw=it.desc,
                price_cents=it.price_cents,
                currency=it.currency,
            )
            db.add(item)

        db.commit()
        return {"restaurant_id": str(rest.id), "count": len(body.items)}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/{restaurant_id}")
async def get_menu(restaurant_id: str):
    """Get menu items for a restaurant"""
    db = next(get_db())

    try:
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        items = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()

        return {
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name,
            },
            "items": [
                {
                    "id": item.id,
                    "title": item.title_raw,
                    "description": item.description_raw,
                    "price_cents": item.price_cents,
                    "currency": item.currency,
                }
                for item in items
            ],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
