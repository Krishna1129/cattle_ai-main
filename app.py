import os
import base64
from io import BytesIO
import numpy as np  # Add numpy import
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
from flask import Flask, render_template, request, jsonify, url_for
from body_structure_analyzer import BodyStructureAnalyzer

# Initialize Flask application
app = Flask(__name__)

# Basic Configuration
app.config.update(
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # 10MB max file size
    UPLOAD_FOLDER=os.path.join('static', 'uploads'),
    SECRET_KEY=os.urandom(24),
    DEBUG=False,
    TESTING=False,
    SEND_FILE_MAX_AGE_DEFAULT=0
)

# Configure logging
import logging
app.logger.setLevel(logging.INFO)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Model Configuration
class ModelConfig:
    MEAN = [0.485, 0.456, 0.406]
    STD = [0.229, 0.224, 0.225]
    IMAGE_SIZE = (224, 224)
    
    # Class names
    CATTLE_CLASSES = ['Buffalo', 'Cow', 'None']
    BREED_NAMES = [
        'Alambadi', 'Amritmahal', 'Ayrshire', 'Banni', 'Bargur', 
        'Bhadawari', 'Brown_Swiss', 'Dangi', 'Deoni', 'Gir', 
        'Guernsey', 'Hallikar', 'Hariana', 'Holstein_Friesian', 
        'Jaffrabadi', 'Jersey', 'Kangayam', 'Kankrej', 'Kasargod', 
        'Kenkatha', 'Kherigarh', 'Khillari', 'Krishna_Valley', 
        'Malnad_gidda', 'Mehsana', 'Murrah', 'Nagori', 'Nagpuri', 
        'Nili_Ravi', 'Nimari', 'Ongole', 'Pulikulam', 'Rathi', 
        'Red_Dane', 'Red_Sindhi', 'Sahiwal', 'Surti', 'Tharparkar', 
        'Toda', 'Umblachery', 'Vechur'
    ]
    
    @classmethod
    def get_transform(cls):
        return transforms.Compose([
            transforms.Resize(cls.IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(cls.MEAN, cls.STD)
        ])

# Model Loading Functions
def load_cattle_model(model_path):
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 3)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    return model

def load_breed_model(model_path, num_classes):
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    return model

# Initialize models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cattle_model = load_cattle_model(os.path.join(BASE_DIR, 'models', 'best_cow_buffalo_none_classifier.pth'))
breed_model = load_breed_model(os.path.join(BASE_DIR, 'models', 'breed_classifier.pth'), len(ModelConfig.BREED_NAMES))

# Initialize body structure analyzer
body_analyzer = BodyStructureAnalyzer()

# -----------------------------
# Prediction Functions
# -----------------------------
def predict_cattle(image):
    transform = ModelConfig.get_transform()
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = cattle_model(image)
        probs = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probs, 1)
        return ModelConfig.CATTLE_CLASSES[predicted.item()], confidence.item()

def predict_breed(image):
    transform = ModelConfig.get_transform()
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = breed_model(image)
        probs = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probs, 1)
        return ModelConfig.BREED_NAMES[predicted.item()], confidence.item()

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    try:
        app.logger.info('Received prediction request')
        
        if 'file' not in request.files:
            app.logger.warning('No file in request')
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            app.logger.warning('Empty filename')
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            app.logger.warning(f'Invalid file format: {file.filename}')
            return jsonify({'error': 'Invalid file format'}), 400

        # Read and process the image
        image_data = file.read()
        if len(image_data) > 10 * 1024 * 1024:  # 10MB
            app.logger.warning('File too large')
            return jsonify({'error': 'File too large'}), 400

        try:
            image = Image.open(BytesIO(image_data)).convert('RGB')
        except Exception as e:
            app.logger.error(f'Error processing image: {str(e)}')
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Make predictions
        cattle_type, cattle_confidence = predict_cattle(image)
        app.logger.info(f'Cattle prediction: {cattle_type} with confidence {cattle_confidence:.3f}')
        
        # Only predict breed if it's a cow or buffalo with high confidence
        breed_name = None
        breed_confidence = None
        if cattle_confidence >= 0.60 and cattle_type in ['Cow', 'Buffalo']:
            app.logger.info(f'Attempting breed prediction for {cattle_type}')
            breed_name, breed_conf = predict_breed(image)
            breed_confidence = f"{breed_conf*100:.2f}%"
            app.logger.info(f'Breed prediction: {breed_name} with confidence {breed_conf:.3f}')
        else:
            app.logger.info(f'Skipping breed prediction - confidence too low ({cattle_confidence:.3f}) or not cattle/buffalo ({cattle_type})')
        
        # Convert image to base64 for display
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        response_data = {
            'success': True,
            'cattle_type': cattle_type,
            'cattle_confidence': f"{cattle_confidence*100:.2f}%",
            'image': img_str
        }
        
        # Add breed information if available
        if breed_name and breed_confidence:
            response_data['breed'] = breed_name
            response_data['breed_confidence'] = breed_confidence
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_structure', methods=['POST'])
def analyze_structure():
    """Handle image upload and body structure analysis"""
    try:
        app.logger.info('Received body structure analysis request')
        
        if 'file' not in request.files:
            app.logger.warning('No file in request')
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            app.logger.warning('Empty filename')
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            app.logger.warning(f'Invalid file format: {file.filename}')
            return jsonify({'error': 'Invalid file format'}), 400

        # Read and process the image
        image_data = file.read()
        if len(image_data) > 10 * 1024 * 1024:  # 10MB
            app.logger.warning('File too large')
            return jsonify({'error': 'File too large'}), 400

        try:
            image = Image.open(BytesIO(image_data)).convert('RGB')
        except Exception as e:
            app.logger.error(f'Error processing image: {str(e)}')
            return jsonify({'error': 'Invalid image file'}), 400
        
        # First, classify the animal
        cattle_type, cattle_confidence = predict_cattle(image)
        
        # If animal type is "None", return early with classification only
        if cattle_type == 'None':
            app.logger.info(f'Animal type is None (confidence: {cattle_confidence:.3f}) - skipping body structure analysis')
            
            # Convert image to base64 for display
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return jsonify({
                'success': True,
                'cattle_type': cattle_type,
                'cattle_confidence': f"{cattle_confidence*100:.2f}%",
                'image': img_str,
                'message': 'No animal detected in the image. Body structure analysis skipped.'
            })
        
        # Get breed if confidence is high enough
        breed_name = "Unknown"
        if cattle_confidence >= 0.60 and cattle_type in ['Cow', 'Buffalo']:
            breed_name, _ = predict_breed(image)
        
        # Perform body structure analysis
        app.logger.info('Starting body structure analysis')
        keypoints = body_analyzer.detect_keypoints(image)
        
        if keypoints:
            # Calculate measurements (using a default scale - in production, this would be calibrated)
            reference_scale = 100.0  # pixels per meter (approximate)
            measurements = body_analyzer.calculate_measurements(
                keypoints, image.width, image.height, reference_scale
            )
            
            # Generate visualization
            vis_image = body_analyzer.visualize_measurements(image, keypoints, measurements)
            
            # Convert visualization to base64
            buffered = BytesIO()
            vis_image.save(buffered, format="JPEG")
            vis_img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Generate report
            report = body_analyzer.generate_report(measurements, cattle_type, breed_name)
            
            # Calculate ATC score
            app.logger.info('Calculating ATC score')
            atc_results = body_analyzer.calculate_atc_score(keypoints, measurements, image, cattle_type)
            
            return jsonify({
                'success': True,
                'cattle_type': cattle_type,
                'cattle_confidence': f"{cattle_confidence*100:.2f}%",
                'breed': breed_name,
                'measurements': measurements,
                'keypoints': keypoints,
                'visualization': vis_img_str,
                'report': report,
                'atc_score': atc_results
            })
        else:
            app.logger.warning('Could not detect keypoints')
            return jsonify({
                'success': False,
                'error': 'Could not detect animal body structure in the image'
            }), 400
    
    except Exception as e:
        app.logger.error(f"Body structure analysis error: {str(e)}")
        return jsonify({'error': 'An error occurred during body structure analysis'}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)