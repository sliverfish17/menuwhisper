from typing import Optional

from app.db import get_db
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.get("")
async def recommend_items(
    q: Optional[str] = Query(None, description="Query text for semantic search"),
    k: int = Query(10, ge=1, le=50, description="Number of results to return"),
    restaurant_id: Optional[str] = Query(None, description="Filter by restaurant ID"),
    user_id: Optional[str] = Query(
        None, description="User ID for personalized recommendations"
    ),
):
    """Get semantic recommendations for menu items"""
    db = next(get_db())

    try:
        # Build filters
        filters = []
        params = {"k": k}

        if restaurant_id:
            filters.append("mi.restaurant_id = :restaurant_id")
            params["restaurant_id"] = restaurant_id

        filters_sql = " AND " + " AND ".join(filters) if filters else ""

        # Text-based similarity search (will upgrade to vector later)
        ann_sql = text(
            f"""
        SELECT 
            mi.id as menu_item_id,
            mi.title, mi.title_raw, mi.description, mi.description_raw,
            mi.price_cents, mi.currency,
            -- Simple text similarity score
            CASE 
                WHEN :use_q = 1 AND (
                    LOWER(mi.title_raw) LIKE LOWER('%' || :query_text || '%') OR 
                    LOWER(mi.description_raw) LIKE LOWER('%' || :query_text || '%')
                ) THEN 0.9
                WHEN :use_q = 1 THEN 0.3
                ELSE 0.5 
            END AS score
        FROM menu_items mi
        WHERE 1=1 {filters_sql}
        ORDER BY score DESC, mi.created_at DESC
        LIMIT :k
        """
        )

        params.update(
            {
                "query_text": q or "",
                "use_q": 1 if q else 0,
            }
        )

        rows = db.execute(ann_sql, params).mappings().all()

        return {
            "items": [
                {
                    "id": str(r["menu_item_id"]),
                    "title": r["title"] or r["title_raw"],
                    "desc": r["description"] or r["description_raw"],
                    "price_cents": r["price_cents"],
                    "currency": r["currency"],
                    "score": r["score"],
                }
                for r in rows
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
