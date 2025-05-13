import pdfplumber
import docx
import io
import streamlit as st

def read_resume(uploaded_file):
    """
    Read the content of the uploaded resume file based on its format.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
        
    Returns:
        str: The extracted text content of the resume
    """
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_extension == 'pdf':
            return read_pdf(uploaded_file)
        elif file_extension == 'docx':
            return read_docx(uploaded_file)
        elif file_extension == 'txt':
            return read_txt(uploaded_file)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        raise

def read_pdf(pdf_file):
    """Extract text from PDF files using pdfplumber"""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        raise Exception(f"PDF reading error: {str(e)}")

def read_docx(docx_file):
    """Extract text from DOCX files using python-docx"""
    try:
        doc = docx.Document(io.BytesIO(docx_file.getvalue()))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        # Also extract tables if present
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + " "
                text += "\n"
                
        return text
    except Exception as e:
        raise Exception(f"DOCX reading error: {str(e)}")

def read_txt(txt_file):
    """Extract text from TXT files"""
    try:
        text = txt_file.getvalue().decode('utf-8')
        return text
    except Exception as e:
        raise Exception(f"TXT reading error: {str(e)}")