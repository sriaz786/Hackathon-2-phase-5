# Deploying to Vercel

This guide explains how to deploy your Next.js + Python (FastAPI) application to Vercel.

## 1. Project Setup (Already Done)

The following files have been created/updated to support Vercel deployment:

- `vercel.json`: Configures Vercel to build both Frontend and Backend.
- `api/index.py`: Entry point for the Python Backend (Serverless Function).
- `requirements.txt`: Python dependencies for Vercel.
- `backend/app/core/config.py`: Updated to support CORS via environment variables.
- `frontend/lib/api.ts`: Updated to use `NEXT_PUBLIC_API_URL`.

## 2. Push to GitHub

Ensure all these changes are committed and pushed to your GitHub repository.

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push
```

## 3. Vercel Dashboard Deployment

1.  **Log in to Vercel** and click **"Add New..."** -> **"Project"**.
2.  **Import** your Git repository.
3.  **Configure Project**:
    - **Root Directory**: Leave it as the root (`./`).
    - **Framework Preset**: Select **Next.js**.
    - **Build & Output Settings**: You can usually leave these as default. The `vercel.json` file will help guide the build.

4.  **Environment Variables**:
    You MUST set the following environment variables in the Vercel project settings:

    **Backend Variables**:
    - `DATABASE_URL`: Your full Neon PostgreSQL connection string (postgres://...).
    - `SECRET_KEY`: A random secret string for security.
    - `ALGORITHM`: `HS256` (default).
    - `BACKEND_CORS_ORIGINS`: Comma-separated list of allowed origins. INITIALLY, you might want to allow all temporarily to test: `*`. Once you have your Vercel domain (e.g., `https://project.vercel.app`), update this to: `https://project.vercel.app,http://localhost:3000`.

    **Frontend Variables**:
    - `NEXT_PUBLIC_API_URL`: The URL of your API.
      - If your frontend and backend are on the same Vercel deployment, setting this to `/api/v1` (relative path) is recommended.
      - Value: `/api/v1`

5.  **Deploy**: Click **Deploy**.

## 4. Troubleshooting

- **500 Errors on API**: Check Vercel **Logs** tab. It often indicates missing dependencies or database connection failures.
- **CORS Errors**: Ensure `BACKEND_CORS_ORIGINS` includes your Vercel app domain (no trailing slash).
- **Database**: Ensure your Neon database is active and the `DATABASE_URL` is correct.

## 5. Local Development

You can still run locally:

- **Frontend**: `cd frontend && npm run dev`
- **Backend**: `cd backend && python -m uvicorn main:app --reload` (or similar command)
