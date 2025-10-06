from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import MenuItem, User, UserFeedback

router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackBody(BaseModel):
    user_id: UUID | None = None
    email: str | None = None
    menu_item_id: UUID
    liked: bool


@router.post("")
def leave_feedback(body: FeedbackBody, db: Session = Depends(get_db)):
    user = None
    if body.user_id:
        user = db.query(User).get(body.user_id)
    if not user and body.email:
        user = db.query(User).filter_by(email=body.email).first()
        if not user:
            user = User(email=body.email)
            db.add(user)
            db.flush()
    if not user:
        raise HTTPException(400, detail="provide user_id or email")

    item = db.query(MenuItem).get(body.menu_item_id)
    if not item:
        raise HTTPException(404, detail="menu_item_not_found")

    existing = db.query(UserFeedback).filter_by(user_id=str(user.id), menu_item_id=item.id).first()
    if existing:
        existing.liked = body.liked
    else:
        db.add(UserFeedback(user_id=str(user.id), menu_item_id=item.id, liked=body.liked))
    db.commit()
    return {"user_id": str(user.id), "menu_item_id": str(item.id), "liked": body.liked}
