"""
Utility functions for the Resume Parser application.
Contains helper methods used across different modules.
"""

import os
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv


def load_api_key() -> str:
    """
    Load Cohere API key from environment variables.
    
    Returns:
        API key string
    
    Raises:
        ValueError: If API key is not found
    """
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key:
        raise ValueError(
            "Cohere API key not found. Please add COHERE_API_KEY to your .env file."
        )
    
    return api_key


def clean_text(text: str) -> str:
    """
    Clean and normalize text from various resume formats.
    
    Args:
        text: Raw text extracted from resume file
        
    Returns:
        Cleaned text ready for processing
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize bullet points
    text = re.sub(r'[•⁃◦▪▫●]', '* ', text)
    
    # Normalize dashes
    text = re.sub(r'[–—―]', '-', text)
    
    # Fix common OCR/PDF extraction issues
    text = text.replace('|', 'I')  # Fix pipe character often misrecognized as 'I'
    
    # Remove page numbers (common in PDFs)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    # Ensure consistency in section headers (capitalize them)
    sections = ['EDUCATION', 'EXPERIENCE', 'SKILLS', 'PROJECTS', 'CERTIFICATIONS', 
                'WORK EXPERIENCE', 'PROFESSIONAL EXPERIENCE', 'ACADEMIC PROJECTS']
    
    for section in sections:
        # Find case-insensitive matches and replace with uppercase version
        pattern = re.compile(re.escape(section), re.IGNORECASE)
        text = pattern.sub(section, text)
    
    return text.strip()


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """
    Extract basic contact information using regex patterns.
    This is a fallback method if the Cohere API doesn't extract this information.
    
    Args:
        text: Cleaned text from resume
        
    Returns:
        Dictionary with extracted email and phone
    """
    contact_info = {
        "email": None,
        "phone": None
    }
    
    # Extract email using regex
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_info["email"] = email_match.group(0)
    
    # Extract phone number (supports various formats)
    phone_patterns = [
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 123-456-7890, 123.456.7890, 123 456 7890
        r'\b\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}\b',  # (123) 456-7890
        r'\b\+\d{1,2}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # +1-123-456-7890
    ]
    
    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)
        if phone_match:
            contact_info["phone"] = phone_match.group(0)
            break
    
    return contact_info


def format_prompt_for_cohere(resume_text: str) -> str:
    """
    Format the resume text into a prompt for the Cohere API.
    
    Args:
        resume_text: Cleaned text from resume
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""
    Parse the following resume and extract these fields:
    - full_name: the candidate's full name
    - email: the candidate's email address
    - phone: the candidate's phone number
    - skills: list of technical and professional skills
    - education: list of education entries with degree, institution, and year
    - experience: list of work experience entries with title, company, duration, and description
    - projects: list of relevant projects (if any)
    - certifications: list of certifications (if any)

    Format the response as JSON.

    Resume:
    {resume_text}
    """
    return prompt


def validate_resume_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean up parsed resume data.
    Ensures that all expected fields are present and in the correct format.
    
    Args:
        data: Dictionary with parsed resume data
        
    Returns:
        Validated and cleaned data dictionary
    """
    # Ensure all expected fields exist (with defaults if missing)
    validated = {
        "full_name": data.get("full_name", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "skills": data.get("skills", []),
        "education": data.get("education", []),
        "experience": data.get("experience", []),
        "projects": data.get("projects", []),
        "certifications": data.get("certifications", [])
    }
    
    # Ensure lists are actually lists
    for field in ["skills", "education", "experience", "projects", "certifications"]:
        if not isinstance(validated[field], list):
            if validated[field]:  # If it has a value but isn't a list
                validated[field] = [validated[field]]
            else:
                validated[field] = []
    
    return validated