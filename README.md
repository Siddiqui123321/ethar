# Inventory & Orders — Submission

Short description: Full-stack Inventory & Order Management app (FastAPI backend, Vite/React frontend, PostgreSQL).

## Public links (fill these before submission)

- GitHub repo: <your-github-repo-url>
- Docker Hub backend image: https://hub.docker.com/r/<DOCKERHUB_USERNAME>/<IMAGE_NAME>
- Live backend URL: <https://your-backend.example.com>
- Live frontend URL: <https://your-frontend.example.com>

## How to run locally (Docker Compose)

1. Copy environment file: `cp .env.example .env`
2. Start services:

```bash
docker-compose up --build
```

3. Backend API: `http://localhost:8000`
4. Frontend: `http://localhost:5173` (or port exposed by your frontend service)

## Docker Hub image link

If you pushed your image to Docker Hub, the public page is:

```
https://hub.docker.com/r/<DOCKERHUB_USERNAME>/<IMAGE_NAME>
```

Replace `<DOCKERHUB_USERNAME>` and `<IMAGE_NAME>` with values you used when pushing. To list local images and see the repository name run:

```powershell
docker images
```

or on Unix:

```bash
docker images | grep <IMAGE_NAME>
```

## Deploying the backend (quick options)

- Render (recommended): Create a new Web Service -> Choose Docker -> set Docker image as `docker.io/<DOCKERHUB_USERNAME>/<IMAGE_NAME>:<TAG>` -> set env var `DATABASE_URL` -> deploy.
- Railway: New Project -> Deploy from Docker image -> supply `docker.io/<DOCKERHUB_USERNAME>/<IMAGE_NAME>:<TAG>` and set envs.
- Fly.io: Use `flyctl deploy --image docker.io/<DOCKERHUB_USERNAME>/<IMAGE_NAME>:<TAG>` or create an app and set image.

Notes: ensure env vars `DATABASE_URL`, `SECRET_KEY` (if any), and `PORT` (if required) are set on the platform.

## Deploying the frontend

- Vercel: Connect your GitHub repo and configure build command `npm run build` and output directory `dist`.
- Netlify: Connect repo or drag deploy the `dist/` folder. Configure build command `npm run build`.

## CI / GitHub Actions (suggestion)

- Backend workflow should: run tests, build Docker image, push to Docker Hub (use `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets).
- Frontend workflow should: run tests/lint, build, and optionally deploy to Netlify/Vercel via their GitHub integrations.

## What to fill before submission

- Replace the placeholders above with your GitHub repo URL, Docker Hub image link, and live frontend/backend URLs.
- Make sure your Docker Hub repo is public so the image page is accessible.

---
If you want, I can now:

1. Create GitHub Actions workflows for backend (tests + push to Docker Hub).
2. Create a small `README` with deploy scripts filled with your actual Docker Hub username and image tag (you'll provide those).
3. Help connect and deploy to Render/Railway/Fly/Vercel — tell me which provider and your Docker Hub image name.

Tell me which of the numbered actions you'd like me to do now and provide your Docker Hub username and image name (or confirm I should leave placeholders).
