from __future__ import annotations

from typing import List


def to_pgvector_str(vec: List[float]) -> str:
    """Convert Python list to PostgreSQL vector string format"""
    return "[" + ",".join(f"{x:.6f}" for x in vec) + "]"


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for texts (placeholder for now)"""
    return [[0.1] * 384 for _ in texts]
