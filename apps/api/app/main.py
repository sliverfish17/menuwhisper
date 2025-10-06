from app.routers import feedback as feedback_router
from app.routers import ingest as ingest_router
from app.routers import menu as menu_router
from app.routers import recommend as recommend_router
from app.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MenuWhisper API")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.APP_ENV}


app.include_router(menu_router.router)
app.include_router(recommend_router.router)
app.include_router(ingest_router.router)
app.include_router(feedback_router.router)
