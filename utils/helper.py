import re
import os
import streamlit as st
import json
from pathlib import Path

def ensure_directory_structure():
    """
    Ensure that all necessary directories exist in the project.
    This is helpful for first-time setup.
    """
    # Define all directories that should exist
    directories = [
        "gui",
        "reader",
        "preprocessor",
        "parser",
        "display",
        "exporter",
        "utils"
    ]
    
    # Create directories if they don't exist
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            # Create an __init__.py file to make the directory a package
            with open(os.path.join(directory, "__init__.py"), "w") as f:
                f.write("# Package initialization file")

def extract_email(text):
    """
    Extract email address from text using regex.
    
    Args:
        text (str): Text to search for email
        
    Returns:
        str: Extracted email or empty string if not found
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else ""

def extract_phone(text):
    """
    Extract phone number from text using regex.
    
    Args:
        text (str): Text to search for phone number
        
    Returns:
        str: Extracted phone or empty string if not found
    """
    # This pattern tries to match various phone number formats
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else ""

def extract_linkedin(text):
    """
    Extract LinkedIn profile URL from text using regex.
    
    Args:
        text (str): Text to search for LinkedIn URL
        
    Returns:
        str: Extracted LinkedIn URL or empty string if not found
    """
    linkedin_pattern = r'(https?://)?(www\.)?linkedin\.com/in/[\w-]+'
    match = re.search(linkedin_pattern, text)
    return match.group(0) if match else ""

def is_valid_json(json_str):
    """
    Check if a string is valid JSON.
    
    Args:
        json_str (str): String to check
        
    Returns:
        bool: True if valid JSON, False otherwise
    """
    try:
        json.loads(json_str)
        return True
    except:
        return False

def get_file_extension(filename):
    """
    Get the file extension from a filename.
    
    Args:
        filename (str): Name of the file
        
    Returns:
        str: File extension in lowercase
    """
    return Path(filename).suffix.lower()[1:]  # Remove the dot

def truncate_text(text, max_length=100):
    """
    Truncate text to a maximum length and add ellipsis if needed.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."