# MenuWhisper (v0.1)


## Run infra + API
cd infra
docker compose up -d --build
# API auto-runs alembic and exposes http://localhost:8000/health


## Run web (Next.js)
cd ../apps/web
pnpm install
pnpm dev # http://localhost:3000


# Check API from web Home page
