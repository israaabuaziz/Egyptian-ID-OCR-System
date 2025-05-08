from flask import Flask, request, jsonify, Response
import json
import werkzeug
import os
from ultralytics import YOLO
import numpy as np
import glob
import pytesseract
from PIL import Image
import shutil
import cv2
import easyocr
from preprocess import preprocess_image
from id import extract_id_info
from waitress import serve  
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Initialize EasyOCR
try:
    easyocr_reader = easyocr.Reader(['ar'])
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except Exception as e:
    logger.error(f"OCR initialization failed: {str(e)}")
    raise

# Load models
try:
    egyptian_id_model_path = r'F:\OCR\detection model\YOLOv8\egy_id_new.pt'
    arabic_numbers_model_path = r'F:\OCR\detection model\YOLOv8\arabic_numbers.pt'
    egyptian_id_model = YOLO(egyptian_id_model_path)
    arabic_numbers_model = YOLO(arabic_numbers_model_path)
except Exception as e:
    logger.error(f"Model loading failed: {str(e)}")
    raise

def clear_previous_predictions():
    """Clear previous YOLO prediction folders"""
    try:
        folders = glob.glob(os.path.join('runs', 'detect', 'predict*'))
        for folder in folders:
            shutil.rmtree(folder, ignore_errors=True)
        logger.info("Previous prediction folders cleared")
    except Exception as e:
        logger.warning(f"Error clearing previous predictions: {str(e)}")

def extract_national_id_number(national_image_path):
    """Extract national ID number using YOLO"""
    try:
        results = arabic_numbers_model(
            national_image_path,
            save=True,
            conf=0.4,
            imgsz=480
        )

        national_id = ''
        for res in results:
            xyxy = res.boxes.xyxy.cpu().numpy()
            sorted_indices = np.argsort(xyxy[:, 0])
            sorted_classes = res.boxes.cls[sorted_indices]
            national_id = ''.join(map(str, sorted_classes.cpu().numpy().astype(int)))

        return national_id
    except Exception as e:
        logger.error(f"Error extracting national ID: {str(e)}")
        return None

def extract_text_from_image(image_path, field_name):
    """Extract text from image using OCR"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
            
        preprocessed_image = preprocess_image(image, field_name)

        if field_name.lower() not in ["firstname"]:
            return pytesseract.image_to_string(preprocessed_image, lang='ara').strip()
        else:
            result = easyocr_reader.readtext(preprocessed_image, detail=0)
            return ' '.join(result).strip()
    except Exception as e:
        logger.error(f"Error extracting text from {field_name}: {str(e)}")
        return ""

@app.route('/api/process-id', methods=['POST'])
def process_id():
    """Main API endpoint for ID processing"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # Save uploaded file
    image_file = request.files['image']
    filename = werkzeug.utils.secure_filename(image_file.filename)
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    temp_path = os.path.join(uploads_dir, filename)
    
    try:
        image_file.save(temp_path)
        clear_previous_predictions()
        
        # Detect and crop ID fields
        egyptian_id_model(
            temp_path,
            save=True,
            conf=0.6,
            imgsz=480,
            show=False,
            save_crop=True
        )
        
        # Process crops
        crops_folder = os.path.join('runs', 'detect')
        skip_fields = {"pic", "egyptian-id", "national_id", "manfucturing_id"}
        
        prediction_folders = sorted(
            glob.glob(os.path.join(crops_folder, 'predict*')),
            key=os.path.getctime,
            reverse=True
        )
        
        if not prediction_folders:
            return jsonify({'error': 'No ID detected in the image'}), 400

        crops_path = os.path.join(prediction_folders[0], 'crops')
        extracted_info = {}
        national_id_number = None

        # Process national ID if found
        national_id_crop = os.path.join(crops_path, 'National_ID')
        if os.path.exists(national_id_crop):
            national_images = glob.glob(os.path.join(national_id_crop, '*.jpg'))
            if national_images:
                national_id_number = extract_national_id_number(national_images[0])
                if national_id_number:
                    extracted_info['national_id'] = national_id_number

        # Process other fields
        if os.path.exists(crops_path):
            for field_folder in os.listdir(crops_path):
                if field_folder.lower() in skip_fields:
                    continue

                field_path = os.path.join(crops_path, field_folder)
                if os.path.isdir(field_path):
                    for image_path in glob.glob(os.path.join(field_path, '*.jpg')):
                        text = extract_text_from_image(image_path, field_folder)
                        extracted_info[field_folder] = text

        # Add additional ID info if available
        if national_id_number:
            id_info = extract_id_info(national_id_number)
            if id_info:
                extracted_info.update(id_info)

        # Create proper JSON response with Arabic characters
        response = Response(
            response=json.dumps(extracted_info, ensure_ascii=False),
            status=200,
            mimetype='application/json; charset=utf-8'
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
    finally:
        # Cleanup resources
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if prediction_folders and os.path.exists(prediction_folders[0]):
                shutil.rmtree(prediction_folders[0], ignore_errors=True)
        except Exception as e:
            logger.warning(f"Cleanup error: {str(e)}")

if __name__ == '__main__':
    # Run with production server for Windows
    if os.getenv('FLASK_ENV') == 'development':
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.info("Starting production server...")
        serve(app, host='0.0.0.0', port=5000)