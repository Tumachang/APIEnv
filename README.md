
# FastAPI on GitHub Codespaces (Dockerfile) → Deploy to Render

This repository bootstraps a **Python + FastAPI** development environment in **GitHub Codespaces** using a single **Dockerfile** and includes instructions to deploy the same image to **Render** as a Web Service.

## Local / Codespaces Development

1. Open the repo in **GitHub Codespaces**. The dev container builds from the root `Dockerfile`.
2. Start the app (hot-reload for development):

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Preview: open `http://localhost:8000` (Codespaces will forward port 8000).

## API examples (no health-check endpoint)

- `GET /` → returns app info (name, version, timestamp)
- `GET /api/items/{item_id}?q=foo`
- `POST /api/echo` with `{ "message": "hello" }`

> Note: Intentionally **no** `/health` endpoint, per requirement.

## Deploy to Render (Docker runtime)

1. Push this repo to GitHub.
2. In the **Render Dashboard** → **New → Web Service**.
   - **Runtime/Language**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Start Command**: leave empty (Render uses Dockerfile `CMD`).
3. Render sets a `PORT` environment variable automatically. Our Dockerfile uses `--host 0.0.0.0 --port $PORT` so the service binds correctly.
4. (Optional) Create `render.yaml` for Blueprint deploys.

## Production notes

- The Dockerfile uses production `uvicorn` (no `--reload`).
- For development (Codespaces), use the command with `--reload` shown above.

## GitHub setup

```bash
git init
git add .
git commit -m "feat: fastapi codespaces + render scaffold"
git branch -M main
git remote add origin <your_repo_url>
git push -u origin main
```
