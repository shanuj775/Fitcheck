# Fitcheck - Deployment Guide

This guide covers deploying Fitcheck on Vercel (frontend) and Render (backend).

## Architecture

```
┌─────────────────────────────────────────┐
│ Vercel (Frontend - React/Vite)         │
│ ├── React 18 App                        │
│ ├── PDF Upload UI                       │
│ └── KB Editor Interface                 │
└──────────────────┬──────────────────────┘
                   │ API Calls
                   ▼
┌─────────────────────────────────────────┐
│ Render (Backend - FastAPI/Python)      │
│ ├── POST /factcheck (PDF processing)   │
│ ├── GET /kb (load knowledge base)      │
│ ├── POST /kb (save knowledge base)     │
│ └── GET /health (health check)         │
└─────────────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ data/knowledge.json  │
        │ (Persistent Storage) │
        └──────────────────────┘
```

## Prerequisites

- GitHub account (for version control)
- Vercel account (free at https://vercel.com)
- Render account (free at https://render.com)

## Step 1: Backend Deployment on Render

### 1.1 Create a Render Account
- Go to https://render.com and sign up
- Connect your GitHub account

### 1.2 Deploy Backend
1. Push your code to GitHub (already done ✓)
2. On Render dashboard, click "New +"
3. Select "Web Service"
4. Connect your Fitcheck GitHub repository
5. Configure:
   - **Name:** `fitcheck-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirement.txt`
   - **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Region:** Select your preferred region
   - **Plan:** Free (or paid for better performance)
6. Click "Create Web Service"
7. Wait for deployment (2-3 minutes)
8. Copy your backend URL (e.g., `https://fitcheck-backend.onrender.com`)

### 1.3 Verify Backend
- Visit `https://fitcheck-backend.onrender.com/health`
- Should return: `{"status":"ok"}`

## Step 2: Frontend Deployment on Vercel

### 2.1 Create a Vercel Account
- Go to https://vercel.com and sign up
- Connect your GitHub account

### 2.2 Deploy Frontend
1. On Vercel dashboard, click "Add New..."
2. Select "Project"
3. Import your Fitcheck GitHub repository
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `./frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`
5. Add Environment Variables:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://fitcheck-backend.onrender.com` (your Render backend URL)
6. Click "Deploy"
7. Wait for deployment (1-2 minutes)
8. Your frontend will be at a URL like `https://fitcheck-xxxxx.vercel.app`

### 2.3 Verify Frontend
- Visit your Vercel URL
- You should see the TruthLayer AI interface
- The app should communicate with the Render backend

## Step 3: Test Full Deployment

1. Open your Vercel URL
2. Select a PDF file
3. Click "Upload and Fact Check"
4. Verify that:
   - Claims are extracted ✓
   - Results are displayed ✓
   - "Load KB" button works ✓
   - "Save KB" persists entries ✓
5. Download CSV export ✓

## Step 4: Custom Domain (Optional)

### On Vercel:
1. Go to Project Settings
2. Click "Domains"
3. Add your custom domain
4. Follow DNS setup instructions

### On Render:
1. Go to Service Settings
2. Click "Custom Domains"
3. Add your custom domain
4. Update backend URL in Vercel environment variables

## Troubleshooting

### Frontend can't reach backend
- **Issue:** CORS errors or connection timeout
- **Solution:** 
  1. Verify backend URL is correct in Vercel env vars
  2. Check Render backend is running (visit `/health`)
  3. Ensure Render backend has CORS enabled (already configured ✓)

### Backend is slow to start
- **Issue:** First request takes 10-30 seconds
- **Solution:** This is normal for free Render tier. Upgrade to paid plan for faster starts.

### Knowledge base not persisting
- **Issue:** KB entries are lost after restart
- **Solution:** Render keeps persistent storage in `/data/` directory. Ensure `data/knowledge.json` exists.

### PDF upload fails
- **Issue:** 413 Payload Too Large
- **Solution:** 
  1. Contact Render support for size limit increase
  2. Or compress PDF before upload

## Environment Variables

### Vercel (.env)
```
VITE_API_URL=https://your-render-backend-url.onrender.com
```

### Render (.env)
```
PYTHONUNBUFFERED=true
```

## Local Development After Deployment

To run locally while pointing to deployed backend:
```bash
# In frontend directory
VITE_API_URL=https://fitcheck-backend.onrender.com npm run dev

# In root directory (backend)
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

## Monitoring & Logs

### Vercel Logs
- Dashboard → Project → Deployments → View Logs
- Real-time logs visible during and after deployment

### Render Logs
- Dashboard → fitcheck-backend → Logs tab
- Stream live logs to monitor requests

## Cost

- **Vercel:** Free tier includes 100 GB bandwidth/month
- **Render:** Free tier includes 750 hours/month (one service can run continuously)
- **Total Monthly Cost:** ~$0 (free tier sufficient for most use cases)

## Next Steps

1. Set up GitHub Actions for automated deployments
2. Add monitoring/alerting (Sentry, LogRocket)
3. Implement database for persistent KB (MongoDB, PostgreSQL)
4. Add authentication for KB editor
5. Implement rate limiting for API endpoints

## Support

For issues:
- Vercel docs: https://vercel.com/docs
- Render docs: https://render.com/docs
- FastAPI docs: https://fastapi.tiangolo.com
- React docs: https://react.dev

---

**Deployment Status:** Ready for production ✓
