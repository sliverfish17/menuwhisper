from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings


app = FastAPI(title="MenuWhisper API")


origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


@app.get("/health")
async def health():
return {"status": "ok", "env": settings.APP_ENV}
