# 🚀 Quick Deployment - 5 Minutes

## One-Click Deployment Steps

### Step 1: Deploy Backend on Render (2 min)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. **Select Repository:** shanuj775/Fitcheck
5. **Configuration:**
   - Name: `fitcheck-backend`
   - Build Command: `pip install -r requirement.txt`
   - Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
6. Click "Deploy Web Service"
7. ⏳ Wait 2-3 minutes for deployment
8. ✅ Copy your backend URL (e.g., https://fitcheck-backend.onrender.com)

### Step 2: Deploy Frontend on Vercel (2 min)

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. **Select Repository:** shanuj775/Fitcheck
5. **Configure:**
   - Framework: Vite
   - Root Directory: `frontend`
   - Build: `npm run build`
   - Output: `dist`
6. **Environment Variables:**
   - Add: `VITE_API_URL` = `https://fitcheck-backend.onrender.com` (your Render URL from Step 1)
7. Click "Deploy"
8. ⏳ Wait 1-2 minutes
9. ✅ Get your frontend URL (e.g., https://fitcheck-xxxxx.vercel.app)

### Step 3: Test Deployment (1 min)

1. Open your Vercel URL
2. Upload a PDF
3. Verify:
   - ✅ Claims extracted
   - ✅ Results displayed
   - ✅ "Load KB" works
   - ✅ "Save KB" persists

Done! 🎉

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot reach backend" | Check VITE_API_URL env var in Vercel matches your Render URL |
| "Slow first request" | Normal on free Render tier; upgrade for faster starts |
| "PDF upload fails" | File too large; try smaller PDF or upgrade Render plan |
| "KB entries lost" | Render persists files automatically; reload page to refresh |

---

## Monitoring

- **Vercel:** Dashboard → Deployments → View Logs
- **Render:** Dashboard → Service → Logs

---

## Next: Custom Domain

Visit DEPLOYMENT.md for optional custom domain setup and advanced configuration.
