import os
import logging
import time
from flask import current_app

# Configure logging
logger = logging.getLogger(__name__)

# In-memory storage for mock S3 operations
mock_s3_storage = {}

def upload_file_to_s3(file_obj, s3_path):
    """
    Mock function to simulate uploading a file to S3.
    
    Args:
        file_obj: File-like object to upload
        s3_path: Path in S3 bucket (e.g., 'folder/filename.jpg')
        
    Returns:
        tuple: (success, message) - boolean indicating success and informational message
    """
    try:
        # Reset file pointer to beginning
        file_obj.seek(0)
        
        # In a real implementation, we would upload to S3
        # For this mock version, we'll just log the action
        logger.info(f"Mock S3 upload: {s3_path}")
        
        # Store the filename in our mock storage
        mock_s3_storage[s3_path] = {
            'upload_time': time.time(),
            'content_type': getattr(file_obj, 'content_type', 'application/octet-stream')
        }
        
        return True, f"File uploaded to {s3_path}"
    
    except Exception as e:
        logger.error(f"Error in mock S3 upload: {str(e)}")
        return False, str(e)

def get_file_url(s3_path, expiration=3600):
    """
    Generate a mock URL for an S3 object.
    
    Args:
        s3_path: Path to object in S3 bucket
        expiration: URL expiration time in seconds (default: 1 hour)
        
    Returns:
        str: Mock URL or None if error
    """
    try:
        # Check if the file exists in our mock storage
        if s3_path not in mock_s3_storage:
            logger.warning(f"File not found in mock S3: {s3_path}")
            return None
        
        # In a real implementation, we would generate a presigned URL
        # For this mock version, we'll return a placeholder URL
        mock_url = f"https://mock-s3-bucket.example.com/{s3_path}?expiry={int(time.time()) + expiration}"
        
        return mock_url
    
    except Exception as e:
        logger.error(f"Error generating mock URL: {str(e)}")
        return None

def list_files(prefix=''):
    """
    List files in mock S3 storage with given prefix.
    
    Args:
        prefix: Folder prefix to list (e.g., 'student_photos/')
        
    Returns:
        list: List of file keys in the mock storage with the given prefix
    """
    try:
        # Filter files by prefix
        matching_files = [key for key in mock_s3_storage.keys() if key.startswith(prefix)]
        
        return matching_files
    
    except Exception as e:
        logger.error(f"Error listing mock S3 files: {str(e)}")
        return []

def delete_file(s3_path):
    """
    Delete a file from mock S3 storage.
    
    Args:
        s3_path: Path to object in mock S3 storage
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if the file exists in our mock storage
        if s3_path not in mock_s3_storage:
            logger.warning(f"File not found in mock S3: {s3_path}")
            return False
        
        # Remove the file from mock storage
        del mock_s3_storage[s3_path]
        
        logger.info(f"Successfully deleted mock S3 file: {s3_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error deleting mock S3 file: {str(e)}")
        return False
