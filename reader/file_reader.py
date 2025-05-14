"""
File Reader Module for the Resume Parser Application
Handles reading different file types and extracting text content.
"""
import os
import pdfplumber
from docx import Document

class FileReader:
    """A class for reading and extracting text from various file types."""
    
    def read_file(self, file_path):
        """
        Read the content of a file based on its extension.
        
        Args:
            file_path (str): Path to the file to be read
            
        Returns:
            str: Text content of the file or None if the file type is not supported
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        _, file_extension = os.path.splitext(file_path.lower())
        
        if file_extension == '.pdf':
            return self._read_pdf(file_path)
        elif file_extension == '.docx':
            return self._read_docx(file_path)
        elif file_extension == '.txt':
            return self._read_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _read_pdf(self, file_path):
        """
        Extract text from a PDF file.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from the PDF
        """
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
                    text += "\n\n"  # Add spacing between pages
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def _read_docx(self, file_path):
        """
        Extract text from a DOCX file.
        
        Args:
            file_path (str): Path to the DOCX file
            
        Returns:
            str: Extracted text from the DOCX
        """
        try:
            doc = Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs]
            text = "\n".join(paragraphs)
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading DOCX file: {str(e)}")
    
    def _read_txt(self, file_path):
        """
        Read content from a text file.
        
        Args:
            file_path (str): Path to the text file
            
        Returns:
            str: Content of the text file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            # Try with a different encoding if UTF-8 fails
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read().strip()
            except Exception as e:
                raise Exception(f"Error reading text file: {str(e)}")
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")