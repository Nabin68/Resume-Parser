import re

def clean_text(text):
    """
    Clean and normalize the extracted text from a resume.
    
    Args:
        text (str): Raw text extracted from the resume
        
    Returns:
        str: Cleaned and normalized text
    """
    # Convert to string if not already
    if not isinstance(text, str):
        text = str(text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize bullet points
    text = re.sub(r'[•●⦁⁃◦‣▪▹◾◼►→]', '* ', text)
    
    # Remove page numbers (common in PDFs)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    # Normalize newlines (remove excessive newlines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove headers/footers (simple heuristic - might need adjustment)
    # This removes repeated lines that might be headers/footers
    lines = text.split('\n')
    
    # Try to identify and remove headers/footers by looking for repeated lines
    # at the beginning or end of each page
    unique_lines = []
    for line in lines:
        # Skip empty lines and lines that are just whitespace or numbers
        if line.strip() and not re.match(r'^\s*\d+\s*$', line):
            unique_lines.append(line)
    
    # Rejoin the text
    text = '\n'.join(unique_lines)
    
    # Try to identify common section headers for better structure
    section_headers = [
        "EDUCATION", "EXPERIENCE", "WORK EXPERIENCE", "SKILLS", 
        "CERTIFICATIONS", "PROJECTS", "PUBLICATIONS", "ACHIEVEMENTS",
        "PROFESSIONAL SUMMARY", "SUMMARY", "OBJECTIVE",
        "PERSONAL INFORMATION", "CONTACT", "REFERENCES"
    ]
    
    # Ensure section headers are properly formatted
    for header in section_headers:
        # Match case-insensitive header, add consistent formatting
        pattern = re.compile(rf'(?i)\b{re.escape(header)}\b')
        text = pattern.sub(f"\n\n{header.upper()}\n", text)
    
    # Final clean-up
    text = text.strip()
    
    return text