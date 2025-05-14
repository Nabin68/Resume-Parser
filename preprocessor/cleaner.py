"""
Text Preprocessing Module for the Resume Parser
Handles cleaning and formatting of extracted resume text.
"""
import re

class TextCleaner:
    """A class for cleaning and preprocessing resume text."""
    
    def clean_text(self, text):
        """
        Clean and normalize text extracted from resumes.
        
        Args:
            text (str): Raw text extracted from a resume file
            
        Returns:
            str: Cleaned and normalized text
        """
        if not text:
            return ""
        
        # Normalize line breaks
        text = self._normalize_line_breaks(text)
        
        # Replace multiple spaces with a single space
        text = self._normalize_spaces(text)
        
        # Normalize bullet points
        text = self._normalize_bullet_points(text)
        
        # Remove unwanted characters
        text = self._remove_unwanted_chars(text)
        
        # Fix common parsing issues
        text = self._fix_common_issues(text)
        
        return text.strip()
    
    def _normalize_line_breaks(self, text):
        """
        Normalize different types of line breaks to standard format.
        
        Args:
            text (str): Text to normalize
            
        Returns:
            str: Text with normalized line breaks
        """
        # Replace multiple line breaks with two line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Ensure consistent line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        return text
    
    def _normalize_spaces(self, text):
        """
        Normalize spaces in text.
        
        Args:
            text (str): Text to normalize
            
        Returns:
            str: Text with normalized spaces
        """
        # Replace multiple spaces with a single space
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove spaces at the beginning of lines
        text = re.sub(r'\n +', '\n', text)
        
        return text
    
    def _normalize_bullet_points(self, text):
        """
        Normalize different bullet point styles to a standard format.
        
        Args:
            text (str): Text to normalize
            
        Returns:
            str: Text with normalized bullet points
        """
        # Normalize various bullet point characters to standard dashes
        bullet_chars = [r'•', r'●', r'○', r'■', r'□', r'▪', r'▫', r'►', r'▻', r'▶', r'»', r'›']
        for char in bullet_chars:
            text = text.replace(char, '- ')
        
        # Replace multiple dashes with a single dash
        text = re.sub(r'-{2,}', '-', text)
        
        # Ensure space after dash
        text = re.sub(r'-([^ ])', r'- \1', text)
        
        return text
    
    def _remove_unwanted_chars(self, text):
        """
        Remove unwanted characters from text.
        
        Args:
            text (str): Text to clean
            
        Returns:
            str: Cleaned text
        """
        # Remove control characters
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Remove page numbers and footers/headers patterns
        text = re.sub(r'\nPage \d+ of \d+\n', '\n', text)
        text = re.sub(r'\n\d+\n', '\n', text)
        
        return text
    
    def _fix_common_issues(self, text):
        """
        Fix common OCR and parsing issues.
        
        Args:
            text (str): Text to fix
            
        Returns:
            str: Fixed text
        """
        # Fix email addresses that might have been broken
        email_pattern = r'([a-zA-Z0-9_.+-]+)[\s@\n]+([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
        text = re.sub(email_pattern, r'\1@\2', text)
        
        # Fix broken URLs
        url_pattern = r'(https?:\/\/)[\s]+([\w\-\.]+\.[a-zA-Z]{2,})'
        text = re.sub(url_pattern, r'\1\2', text)
        
        # Fix dates that may have been broken across lines
        date_pattern = r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?)\s*\n\s*(\d{4})'
        text = re.sub(date_pattern, r'\1 \2', text)
        
        return text
    
    def segment_resume(self, text):
        """
        Attempt to segment resume into sections.
        Optional feature that can be developed further.
        
        Args:
            text (str): Cleaned resume text
            
        Returns:
            dict: Dictionary with resume sections
        """
        # This is a placeholder for more sophisticated segmentation
        # In a production system, this would use more advanced techniques
        
        sections = {
            'header': '',
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'other': ''
        }
        
        # Simple pattern matching for common section headers
        experience_headers = [
            r'\bEXPERIENCE\b', r'\bWORK EXPERIENCE\b', r'\bEMPLOYMENT\b',
            r'\bPROFESSIONAL EXPERIENCE\b', r'\bWORK HISTORY\b'
        ]
        
        education_headers = [
            r'\bEDUCATION\b', r'\bACADEMIC BACKGROUND\b', r'\bQUALIFICATIONS\b',
            r'\bDEGREES\b', r'\bCERTIFICATIONS\b'
        ]
        
        skills_headers = [
            r'\bSKILLS\b', r'\bTECHNICAL SKILLS\b', r'\bCOMPETENCIES\b',
            r'\bPROFICIENCIES\b', r'\bCAPABILITIES\b'
        ]
        
        # Currently just a placeholder
        # In a real implementation, this function would be more sophisticated
        # and would actually segment the resume text
        
        return sections