import logging
import random
import numpy as np
from io import BytesIO
from PIL import Image
from werkzeug.datastructures import FileStorage

# Configure logging
logger = logging.getLogger(__name__)

def encode_face_image(file):
    """
    Encode a face in an image.
    
    Args:
        file: A FileStorage object or file-like object containing the image
        
    Returns:
        list: Mock face encoding if a face was found, None otherwise
    """
    try:
        # Read image file to verify it's a valid image
        if isinstance(file, FileStorage):
            # Reset file pointer to beginning
            file.seek(0)
            image_data = file.read()
            image = Image.open(BytesIO(image_data))
        else:
            image = Image.open(file)
            
        # For demo purposes, generate a random encoding vector
        # Real face_recognition would generate a 128-dimensional encoding
        encoding = [random.uniform(-1, 1) for _ in range(128)]
        
        logger.info("Generated mock face encoding")
        return encoding
    
    except Exception as e:
        logger.error(f"Error encoding face: {str(e)}")
        return None

def detect_faces_in_image(file):
    """
    Detect all faces in a classroom image.
    
    Args:
        file: A FileStorage object or file-like object containing the image
        
    Returns:
        tuple: (face_locations, face_encodings) - mock lists of face locations and encodings
    """
    try:
        # Read image file to verify it's a valid image
        if isinstance(file, FileStorage):
            # Reset file pointer to beginning
            file.seek(0)
            image_data = file.read()
            image = Image.open(BytesIO(image_data))
        else:
            image = Image.open(file)
            
        # For demo purposes, generate mock data
        # Generate random number of detected faces (1-10)
        num_faces = random.randint(5, 15)
        
        # Mock face locations (format: top, right, bottom, left)
        face_locations = []
        face_encodings = []
        
        for _ in range(num_faces):
            # Generate random face locations
            top = random.randint(0, 300)
            right = random.randint(400, 600)
            bottom = random.randint(top + 100, top + 200)
            left = random.randint(100, right - 100)
            
            face_locations.append((top, right, bottom, left))
            
            # Generate random face encoding for each detected face
            encoding = [random.uniform(-1, 1) for _ in range(128)]
            face_encodings.append(encoding)
        
        logger.info(f"Generated {num_faces} mock face detections")
        return face_locations, face_encodings
    
    except Exception as e:
        logger.error(f"Error detecting faces: {str(e)}")
        return [], []

def compare_faces(known_face_encoding, face_encodings, tolerance=0.6):
    """
    Compare a known face encoding with a list of face encodings.
    
    Args:
        known_face_encoding: Face encoding of a registered student
        face_encodings: List of face encodings from classroom photo
        tolerance: Threshold for face comparison (lower is stricter)
        
    Returns:
        tuple: (is_present, confidence) - boolean indicating if student is present and confidence score
    """
    try:
        if not face_encodings:
            return False, 0
        
        # In mock implementation, use random comparison for demo
        # Real implementation would calculate actual distances
        
        # 70% chance of being recognized if there are faces in the image
        is_present = random.random() < 0.7
        
        # Random confidence between 0.65 and 0.95 if present
        confidence = random.uniform(0.65, 0.95) if is_present else 0
        
        logger.info(f"Mock face comparison result: present={is_present}, confidence={confidence:.2f}")
        return is_present, float(confidence)
    
    except Exception as e:
        logger.error(f"Error comparing faces: {str(e)}")
        return False, 0
