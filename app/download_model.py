"""
Download YOLOv8 model weights.

This script downloads the YOLOv8n model weights from Ultralytics.
Run this before starting the application if the model file doesn't exist.
"""

import os
from pathlib import Path

try:
    from ultralytics import YOLO
    
    MODEL_PATH = Path(__file__).parent / "yolov8n.pt"
    
    if MODEL_PATH.exists():
        print(f"✓ YOLOv8 model already exists at {MODEL_PATH}")
    else:
        print("Downloading YOLOv8n model...")
        model = YOLO("yolov8n.pt")
        print(f"✓ YOLOv8 model downloaded to {MODEL_PATH}")
        
except ImportError:
    print("Error: ultralytics package not found. Install it with:")
    print("pip install ultralytics")
except Exception as e:
    print(f"Error downloading model: {e}")
