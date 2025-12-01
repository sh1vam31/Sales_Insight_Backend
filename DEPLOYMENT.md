# Deployment Guide for Render

This guide will help you deploy the Sales Insights Backend to Render.com.

## Prerequisites

- ✅ PostgreSQL database already deployed on Render
- ✅ GitHub repository with your code
- ✅ Render account

## Step 1: Create a Web Service on Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**:
   - Select your repository: `sh1vam31/Sales_Insight_Backend`
   - Choose the branch: `sales-review` (or `main` if you merge)

## Step 2: Configure the Web Service

### Basic Settings:
- **Name**: `sales-insights-backend` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `sales-review` (or `main`)
- **Root Directory**: Leave empty (root of repo)

### Build & Start Commands:
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

### Environment Variables:
Render will automatically provide:
- `DATABASE_URL` - Your PostgreSQL connection string (automatically set when you link the database)

**Optional Environment Variables:**
- `ENVIRONMENT=production`
- `DEBUG=False`

## Step 3: Link PostgreSQL Database

1. In your Web Service settings, go to **"Environment"** tab
2. Under **"Add Environment Variable"**, you should see an option to **"Link Database"**
3. Select your existing PostgreSQL database
4. Render will automatically set the `DATABASE_URL` environment variable

**OR** manually add:
- **Key**: `DATABASE_URL`
- **Value**: Your PostgreSQL connection string from Render (format: `postgres://user:pass@host:port/dbname`)

## Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start the application
   - Create database tables automatically (via `init_db()`)

## Step 5: Verify Deployment

1. **Check Build Logs**: Ensure build completed successfully
2. **Check Runtime Logs**: Look for "Application startup complete"
3. **Test Health Endpoint**: 
   ```
   https://your-service-name.onrender.com/
   ```
   Should return: `{"message": "Sales Insights Backend Running"}`

4. **Test API Documentation**:
   ```
   https://your-service-name.onrender.com/docs
   ```

## Troubleshooting

### Database Connection Issues

**Problem**: Application fails to connect to PostgreSQL

**Solution**: 
- Verify `DATABASE_URL` is set correctly in Render environment variables
- Check that the database is running and accessible
- The code automatically converts `postgres://` to `postgresql+asyncpg://` - this should work automatically

### Build Failures

**Problem**: Build fails during `pip install`

**Solution**:
- Check `requirements.txt` is in the repository
- Verify all package versions are compatible
- Check build logs for specific error messages

### Application Crashes

**Problem**: App starts but crashes immediately

**Solution**:
- Check runtime logs in Render dashboard
- Verify `DATABASE_URL` is set
- Ensure database tables are created (check logs for `init_db` messages)

### Port Issues

**Problem**: "Port already in use" or connection refused

**Solution**:
- Make sure start command uses `--port $PORT` (Render sets this automatically)
- Use `--host 0.0.0.0` to bind to all interfaces

## Important Notes

1. **Database Tables**: Tables are created automatically on first startup via `init_db()` function
2. **Environment Variables**: `DATABASE_URL` is automatically provided by Render when you link a database
3. **Auto-Deploy**: Render automatically deploys when you push to the connected branch
4. **Free Tier**: Render free tier services spin down after 15 minutes of inactivity (first request may be slow)

## Manual Deployment Steps (if needed)

If you need to manually trigger a deployment:

```bash
# 1. Make sure all changes are committed
git add .
git commit -m "Ready for deployment"

# 2. Push to your branch
git push origin sales-review

# 3. Render will automatically detect the push and deploy
```

## Testing Your Deployed API

Once deployed, you can test using curl or the Swagger UI:

```bash
# Health check
curl https://your-service-name.onrender.com/

# Create a sale
curl -X POST https://your-service-name.onrender.com/api/sales \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Laptop",
    "quantity": 2,
    "price": 999.99,
    "sale_date": "2024-11-27"
  }'

# List all sales
curl https://your-service-name.onrender.com/api/sales
```

## Next Steps

- Set up custom domain (optional)
- Configure SSL (automatic on Render)
- Set up monitoring and alerts
- Configure auto-scaling if needed

