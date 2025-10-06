from __future__ import annotations

from sqlalchemy.orm import Session

from .models import MenuItem, MenuItemEmbedding


def upsert_embeddings_for_restaurant(db: Session, restaurant_id: str) -> int:
    """Create embeddings for all menu items in a restaurant"""
    items = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()

    embedded_count = 0
    for item in items:
        # Check if embedding already exists
        existing = (
            db.query(MenuItemEmbedding)
            .filter(MenuItemEmbedding.menu_item_id == item.id)
            .first()
        )

        if not existing:
            # Create dummy embedding (replace with actual embedding model)
            dummy_embedding = [0.1] * 384  # 384-dimensional vector

            embedding = MenuItemEmbedding(
                menu_item_id=item.id,
                embedding=dummy_embedding,
                embedding_model="dummy-model-v1",
            )
            db.add(embedding)
            embedded_count += 1

    db.commit()
    return embedded_count
