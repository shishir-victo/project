import os
import json
import logging
import numpy as np
from datetime import datetime, date
from flask import current_app
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

class DateTimeEncoder(json.JSONEncoder):
    """Custom encoder for datetime objects to JSON"""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(DateTimeEncoder, self).default(obj)

def generate_filename(prefix, extension):
    """
    Generate a unique filename with timestamp
    
    Args:
        prefix: String prefix for the filename
        extension: File extension (without dot)
        
    Returns:
        str: Secure filename with timestamp
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"{prefix}_{timestamp}.{extension}"
    return secure_filename(filename)

def format_datetime(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Format a datetime object as a string
    
    Args:
        dt: Datetime object
        format_str: Format string (default: YYYY-MM-DD HH:MM:SS)
        
    Returns:
        str: Formatted datetime string
    """
    if not dt:
        return ""
    return dt.strftime(format_str)

def create_folder_if_not_exists(folder_path):
    """
    Create a folder if it doesn't exist
    
    Args:
        folder_path: Path to the folder
        
    Returns:
        bool: True if folder exists or was created, False otherwise
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return True
    except Exception as e:
        logger.error(f"Error creating folder {folder_path}: {str(e)}")
        return False

def calculate_attendance_percentage(present_count, total_sessions):
    """
    Calculate attendance percentage
    
    Args:
        present_count: Number of sessions student was present
        total_sessions: Total number of sessions
        
    Returns:
        float: Attendance percentage (0-100)
    """
    if total_sessions == 0:
        return 0.0
    return round((present_count / total_sessions) * 100, 1)

def get_attendance_status_class(percentage):
    """
    Get Bootstrap class name based on attendance percentage
    
    Args:
        percentage: Attendance percentage (0-100)
        
    Returns:
        str: Bootstrap class name (danger, warning, success)
    """
    if percentage < 75:
        return "danger"
    elif percentage < 90:
        return "warning"
    else:
        return "success"

def paginate(items, page, per_page):
    """
    Paginate a list of items
    
    Args:
        items: List of items to paginate
        page: Current page number (1-based)
        per_page: Number of items per page
        
    Returns:
        tuple: (paginated_items, total_pages)
    """
    page = max(1, page)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    paginated_items = items[start_idx:end_idx]
    total_pages = (len(items) + per_page - 1) // per_page
    
    return paginated_items, total_pages
