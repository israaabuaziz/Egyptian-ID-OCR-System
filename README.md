# Egyptian ID OCR System

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.7.0-orange)
![YOLOv8](https://img.shields.io/badge/YOLOv8-ultralytics-red)
![EasyOCR](https://img.shields.io/badge/EasyOCR-1.6.2-green)

An advanced OCR system for extracting information from Egyptian national ID cards and criminal record documents, with Arabic/English text recognition capabilities.

## Features
- 🪪 Automatic ID field detection with YOLOv8
- 🔢 Arabic numeral recognition and conversion
- 📄 Text extraction from ID fields 

## Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR (install from [here](https://github.com/UB-Mannheim/tesseract/wiki))

### Setup
```bash
# Clone repository
git clone https://github.com/israaabuaziz/egyptian-id-ocr-api.git
cd egyptian-id-ocr-api

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set FLASK_ENV=development  # Windows
export FLASK_ENV=development  # Linux/Mac
