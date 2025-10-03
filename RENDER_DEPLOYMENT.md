# 🚀 Render Deployment Guide - Cattle AI Analyzer

## 📋 Quick Deployment Steps

### **Step 1: Prepare Your Repository**
1. Ensure all files are committed to your Git repository
2. Make sure model files (`*.pth`) are included
3. Verify `requirements.txt` is up to date

### **Step 2: Deploy to Render**

#### **Option A: Deploy via Render Dashboard (Recommended)**

1. **Visit Render Dashboard**
   - Go to: https://dashboard.render.com
   - Sign up/Login with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `model/cattle_buffalo` folder

3. **Configure Service**
   ```
   Name: cattle-ai-analyzer (or your preferred name)
   Environment: Python 3
   Region: Choose closest to your users
   Branch: main/master
   Root Directory: model/cattle_buffalo
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300
   ```

4. **Environment Variables**
   Add these in the Environment tab:
   ```
   FLASK_ENV = production
   MAX_CONTENT_LENGTH = 10485760
   PYTHONUNBUFFERED = 1
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete (~5-10 minutes)

#### **Option B: Deploy via render.yaml (Automated)**

If you have `render.yaml` in your repo:
1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect and deploy using the YAML config

### **Step 3: Verify Deployment**

Your app will be available at:
`https://cattle-ai-analyzer.onrender.com` (or your custom name)

### **Step 4: Test Your API Endpoints**

1. **Home Page**: `GET /`
2. **Cattle Classification**: `POST /predict`
3. **Body Structure Analysis**: `POST /analyze_structure`

## 🔧 Configuration Details

### **Render Service Settings**
- **Plan**: Starter (Free tier) or higher
- **Auto-Deploy**: Yes (deploys on git push)
- **Health Check**: `/` endpoint

### **Build & Start Commands**
```bash
# Build Command
pip install -r requirements.txt

# Start Command  
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300
```

### **Environment Variables**
```env
FLASK_ENV=production
MAX_CONTENT_LENGTH=10485760
PYTHONUNBUFFERED=1
```

## 📊 API Usage Examples

### **1. Basic Cattle Classification**
```bash
curl -X POST https://your-app.onrender.com/predict \
  -F "file=@cow_image.jpg"
```

### **2. Body Structure Analysis**
```bash
curl -X POST https://your-app.onrender.com/analyze_structure \
  -F "file=@cow_image.jpg"
```

### **3. JavaScript/Frontend Integration**
```javascript
const formData = new FormData();
formData.append('file', imageFile);

fetch('https://your-app.onrender.com/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🎯 Features Available After Deployment

✅ **Cattle/Buffalo Classification**
- Identifies: Cow, Buffalo, or None
- Confidence scores for each prediction

✅ **Breed Recognition** 
- 40+ Indian cattle breeds supported
- Automatic breed detection for high-confidence classifications

✅ **Body Structure Analysis**
- Keypoint detection
- Measurement calculations
- ATC score computation
- Visual analysis reports

✅ **Professional Reports**
- Detailed analysis results
- Visualizations with keypoints
- Measurement data
- Breed-specific insights

## 🚨 Important Notes

### **Free Tier Limitations**
- Service sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 750 hours/month limit

### **Upgrade Considerations**
- **Starter Plan ($7/month)**: No sleeping, better performance
- **Standard Plan ($25/month)**: Multiple workers, faster responses

### **File Size Limits**
- Maximum upload: 10MB per image
- Supported formats: JPG, PNG, JPEG

## 🔍 Troubleshooting

### **Common Issues**

1. **Build Failures**
   - Check `requirements.txt` for version conflicts
   - Ensure model files are included in repository
   - Verify Python version compatibility

2. **Memory Issues**
   - PyTorch models require significant RAM
   - Consider upgrading to paid plan for better performance

3. **Timeout Errors**
   - Increase timeout in gunicorn command
   - Optimize image processing code
   - Use smaller model files if possible

4. **Cold Start Delays**
   - Expected on free tier (15+ seconds)
   - Upgrade to paid plan to eliminate sleeping

### **Monitoring & Logs**
- Check Render dashboard for build logs
- Monitor service health in dashboard
- Use Render's built-in metrics

## 🎉 Success!

Once deployed, your Cattle AI Analyzer will be:
- 🌐 **Publicly accessible** worldwide
- 🤖 **AI-powered** cattle analysis
- 📱 **API-ready** for mobile/web apps
- 🔄 **Auto-deploying** on code changes

**Share your deployed URL and let users experience the future of livestock technology!**

---

## 📞 Support Resources

- **Render Documentation**: https://render.com/docs
- **Flask Deployment Guide**: https://flask.palletsprojects.com/en/2.0.x/deploying/
- **PyTorch Deployment**: https://pytorch.org/tutorials/beginner/deploy_model.html

**Happy Deploying! 🚀🐄**

