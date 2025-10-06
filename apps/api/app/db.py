"""
SQLAlchemy engine/session + Base.
"""

from __future__ import annotations
from contextlib import asynccontextmanager
from typing import AsyncIterator


from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from fastapi import Depends
from fastapi import FastAPI


from .settings import settings


class Base(DeclarativeBase):
    pass


# Synchronous SQLAlchemy (simpler for FastAPI sync handlers)
engine = create_engine(settings.DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
