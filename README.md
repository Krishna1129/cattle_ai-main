# 🐄 AI-Powered Cattle Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-orange.svg)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgreen.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-red.svg)](https://opencv.org/)
[![Render](https://img.shields.io/badge/Deploy-Render-purple.svg)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Advanced AI-powered livestock management platform featuring deep learning classification, morphometric analysis, and professional web interface for precision cattle assessment.**

## 📋 Table of Contents
- [🎯 Project Overview](#-project-overview)
- [✨ Key Features](#-key-features)
- [🏗️ System Architecture](#️-system-architecture)
- [️ Technologies Stack](#️-technologies-stack)
- [📊 Model Performance](#-model-performance)
- [🚀 Quick Start](#-quick-start)
- [📖 Usage Guide](#-usage-guide)
- [🎨 User Interface](#-user-interface)
- [📁 Project Structure](#-project-structure)
- [🔧 Configuration](#-configuration)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

## 🎯 Project Overview

This comprehensive cattle analysis platform combines **cutting-edge AI technology** with **computer vision** to provide professional-grade livestock assessment tools. Built with Flask web framework and PyTorch deep learning models, it's designed for farmers, veterinarians, livestock specialists, and agricultural researchers.

### 🎪 Live Demo
```bash
# Local development
python app.py
# Open http://localhost:5000 in your browser
```

### 🌐 **Production Deploy**
**Ready-to-deploy** on Render with one-click deployment using the included `render.yaml` configuration.

## ✨ Key Features

### 🧠 **AI Classification Engine**
- **Cattle vs Buffalo Detection** with high accuracy using CNN models
- **Breed Identification** from multiple cattle and buffalo breeds
- **Real-time confidence scoring** for all predictions
- **Multi-model ensemble** for robust classification

### 📏 **Morphometric Analysis**
- **Body Structure Assessment** using computer vision
- **Comprehensive measurements** and body condition scoring
- **Visual keypoint detection** and analysis
- **Professional assessment reports**

### 🎨 **Professional Web Interface**
- **Modern responsive design** for all devices
- **Drag-and-drop image upload** with real-time preview
- **Interactive results dashboard** with visual analytics
- **Multiple page interface**: Home, About, FAQ, Guide
- **Error handling** with custom 404/500 pages

### 📊 **Analysis Features**
- **Real-time image processing** with progress indicators
- **Detailed analysis reports** with visual overlays
- **Confidence metrics** and quality assessments
- **Professional formatting** for documentation

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Frontend  │────│   Flask Backend  │────│  AI Model Hub   │
│   (HTML/CSS/JS) │    │   (Python/Flask) │    │  (PyTorch CNN)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ • Responsive UI │    │ • Image Upload   │    │ • Cattle Model  │
│ • Multi-page    │    │ • API Endpoints  │    │ • Breed Model   │
│ • Error Pages   │    │ • Model Loading  │    │ • Body Analyzer │
│ • Interactive   │    │ • Result Display │    │ • Preprocessing │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 🔄 **Processing Pipeline**
1. **Image Upload** → Drag-and-drop or file selection
2. **Validation** → Format and size verification  
3. **Preprocessing** → Resize, normalize for model input
4. **AI Analysis** → Cattle classification and breed identification
5. **Body Analysis** → Morphometric measurements and scoring
6. **Results** → Interactive dashboard with detailed insights

## �️ Technologies Stack

### **Backend**
- **Flask 2.3.3** - Web framework
- **PyTorch 2.0.1** - Deep learning models
- **OpenCV 4.8.1** - Computer vision processing
- **Pillow 10.0.1** - Image handling
- **NumPy 1.24.3** - Numerical computations
- **Gunicorn 21.2.0** - Production WSGI server

### **Frontend**
- **HTML5** - Modern semantic markup
- **CSS3** - Responsive design with Grid/Flexbox
- **JavaScript** - Interactive functionality
- **Bootstrap-inspired** - Professional UI components

### **Deployment**
- **Render** - Cloud platform (recommended)
- **Docker** - Containerization support
- **Git** - Version control integration

## 📊 Model Performance

### **Classification Models**
- **Cattle Detection Model**: `best_cow_buffalo_none_classifier.pth`
  - Classes: Buffalo, Cow, None
  - Architecture: CNN-based classifier
  - Input: 224x224 RGB images

- **Breed Classification Model**: `breed_classifier.pth`
  - Multiple breed categories
  - Fine-tuned for livestock identification
  - Confidence threshold: 60%

### **Body Structure Analyzer**
- **Computer vision-based** morphometric analysis
- **Keypoint detection** for body measurements
- **Automated scoring** and assessment
- **Visual overlay** generation

## 🚀 Quick Start

### **Prerequisites**
- Python 3.10+
- Git
- 4GB+ RAM (for model loading)

### **Installation**
```bash
# Clone repository
git clone https://github.com/Krishna1129/cattle_ai-main.git
cd cattle_ai-main

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### **Access Application**
- **Local**: http://localhost:5000
- **Network**: http://0.0.0.0:5000

## � Usage Guide

### **1. Image Upload**
- Navigate to the main page
- Use drag-and-drop or click to select image
- Supported formats: JPG, JPEG, PNG
- Maximum size: 10MB

### **2. Analysis Process**
- Upload triggers automatic processing
- Real-time progress indicators
- AI models analyze the image
- Results appear in interactive dashboard

### **3. Results Interpretation**
- **Classification Results**: Animal type and breed
- **Confidence Scores**: Prediction reliability
- **Body Analysis**: Morphometric measurements
- **Visual Overlays**: Keypoint detection

### **4. Navigation**
- **Home**: Main analysis interface
- **About**: Project information
- **Guide**: Detailed usage instructions  
- **FAQ**: Common questions and answers

## 🎨 User Interface

### **Responsive Design**
- **Desktop**: Full-featured dashboard with sidebar navigation
- **Tablet**: Optimized grid layouts with touch controls
- **Mobile**: Stacked interface with mobile-first design

### **Page Structure**
- **Base Template**: `base.html` - Common layout and navigation
- **Main Interface**: `index.html` - Analysis dashboard
- **Information Pages**: `about.html`, `guide.html`, `faq.html`
- **Error Pages**: `404.html`, `500.html` - Custom error handling

### **Styling**
- **Modern CSS**: `style.css` - Professional styling
- **Interactive JS**: `main.js` - Dynamic functionality
- **Color Scheme**: Professional blue/green palette
- **Typography**: Clean, readable fonts

## 📁 Project Structure

```
cattle_ai-main/
├─ 📄 app.py                          # Flask application entry point
├─ 📄 body_structure_analyzer.py      # Computer vision analysis module
├─ 📄 requirements.txt                # Python dependencies
├─ 📄 runtime.txt                     # Python version specification
├─ 📄 render.yaml                     # Render deployment configuration
├─ 📄 Dockerfile                      # Docker containerization
├─ 📄 RENDER_DEPLOYMENT.md           # Deployment documentation
├─ � README.md                       # Project documentation
│
├─ �📁 models/                          # AI model files
│   ├─ best_cow_buffalo_none_classifier.pth  # Cattle classification model
│   └─ breed_classifier.pth                  # Breed identification model
│
├─ 📁 static/                          # Frontend assets
│   ├─ 📁 css/
│   │   └─ style.css                  # Main stylesheet
│   └─ 📁 js/
│       └─ main.js                    # JavaScript functionality
│
├─ 📁 templates/                       # HTML templates
│   ├─ base.html                      # Base template
│   ├─ index.html                     # Main interface
│   ├─ about.html                     # About page
│   ├─ guide.html                     # Usage guide
│   ├─ faq.html                       # FAQ page
│   └─ 📁 errors/                     # Error pages
│       ├─ 404.html                   # Not found page
│       └─ 500.html                   # Server error page
│
└─ � .git/                           # Git version control
    ├─ .gitignore                     # Git ignore rules
    ├─ .gitattributes                 # Git attributes
    └─ .renderignore                  # Render ignore rules
```

## 🔧 Configuration

### **Application Settings**
```python
# app.py configuration
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB file limit
UPLOAD_FOLDER = 'static/uploads'       # Upload directory
SECRET_KEY = os.urandom(24)            # Session security
DEBUG = False                          # Production mode
```

### **Model Configuration**
```python
# Image preprocessing
IMAGE_SIZE = (224, 224)                # Model input size
CONFIDENCE_THRESHOLD = 0.60             # Minimum prediction confidence

# Normalization (ImageNet standards)
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
```

### **Supported Formats**
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024       # 10MB limit
```

## 🚀 Deployment

### 🌐 **Local Development**
```bash
# Clone the repository
git clone https://github.com/Krishna1129/cattle_ai-main.git
cd cattle_ai-main

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
# Access: http://localhost:5000
```

### ☁️ **Cloud Deployment - Render (Recommended)**

#### **🎯 Quick Deploy**
1. **Fork this repository** to your GitHub account
2. **Visit**: https://dashboard.render.com
3. **Sign up/Login** with GitHub
4. **Create New Web Service** and connect your repository

#### **⚙️ Render Configuration**
```yaml
# render.yaml (already included)
services:
  - type: web
    name: cattle-ai-analyzer
    env: python
    region: oregon
    pythonVersion: "3.10"
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300
```

#### **🔑 Environment Variables**
Set these in Render Dashboard:
```bash
FLASK_ENV=production
MAX_CONTENT_LENGTH=10485760
PYTHONUNBUFFERED=1
```

#### **📋 Deployment Settings**
| Setting | Value |
|---------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300` |
| **Python Version** | `3.10` |
| **Instance Type** | `Starter` (Free) |
| **Auto-Deploy** | `Yes` |

### 🐳 **Docker Deployment**
```bash
# Build image
docker build -t cattle-ai .

# Run container
docker run -p 5000:5000 cattle-ai

# Or use Docker Compose
docker-compose up --build
```

### 🖥️ **Production Deployment**
```bash
# Using Gunicorn (Linux/Mac)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app --timeout 300

# Using Waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### 🌍 **Other Cloud Platforms**

#### **Heroku**
```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
heroku open
```

#### **Railway**
```bash
# Install Railway CLI
railway login
railway init
railway up
```

#### **DigitalOcean App Platform**
1. Connect GitHub repository
2. Use `requirements.txt` for dependencies  
3. Set start command: `gunicorn app:app`

### 📊 **Performance Optimization**
- **Model Optimization**: Use TorchScript for faster inference
- **Caching**: Implement Redis for repeated requests
- **Load Balancing**: Use multiple worker processes
- **CDN**: Serve static assets from CDN
- **Image Optimization**: Compress uploaded images

### 🔒 **Security Considerations**
```python
# Production security settings
import os
from werkzeug.middleware.proxy_fix import ProxyFix

# Enable proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app)

# Set secure headers
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### 📈 **Monitoring & Logging**
```python
# Production logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

### 💰 **Cost Optimization**
- **Free Tier Options**: Render, Railway, Heroku (limited hours)
- **Paid Plans**: Start from $7/month for 24/7 uptime
- **Model Size**: Optimize model files to reduce storage costs
- **Request Caching**: Reduce computational overhead

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

### **🔨 Development Setup**
```bash
# Fork and clone
git clone https://github.com/your-username/cattle_ai-main.git
cd cattle_ai-main

# Create feature branch
git checkout -b feature/your-feature-name

# Install dependencies
pip install -r requirements.txt

# Make changes and test
python app.py

# Submit pull request
```

### **📝 Contribution Guidelines**
- **Code Style**: Follow PEP 8 standards
- **Testing**: Test all new features thoroughly
- **Documentation**: Update README for new capabilities
- **Commits**: Use descriptive commit messages
- **Models**: Ensure model compatibility

### **🎯 Areas for Contribution**
- [ ] **Model Improvements**: Higher accuracy, more breeds
- [ ] **UI/UX**: Enhanced interface, mobile optimization  
- [ ] **Features**: Disease detection, batch processing
- [ ] **Performance**: Faster inference, optimization
- [ ] **Documentation**: Tutorials, API documentation
- [ ] **Testing**: Unit tests, integration tests

### **🐛 Bug Reports**
Use GitHub Issues with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Screenshots if applicable

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyTorch Team** for the deep learning framework
- **OpenCV Community** for computer vision tools
- **Flask Contributors** for the web framework
- **Agricultural Research Community** for domain expertise

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/Krishna1129/cattle_ai-main/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Krishna1129/cattle_ai-main/discussions)
- **Repository**: [GitHub Repository](https://github.com/Krishna1129/cattle_ai-main)

---

<div align="center">

### ⭐ Star this project if it helped you! ⭐

**Made with ❤️ for the agricultural community**

[![GitHub stars](https://img.shields.io/github/stars/Krishna1129/cattle_ai-main.svg?style=social&label=Star)](https://github.com/Krishna1129/cattle_ai-main)
[![GitHub forks](https://img.shields.io/github/forks/Krishna1129/cattle_ai-main.svg?style=social&label=Fork)](https://github.com/Krishna1129/cattle_ai-main/fork)

</div>
