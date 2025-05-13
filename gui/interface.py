import os
import streamlit as st

def create_interface():
    """
    Create the Streamlit interface for the resume parser.
    
    Returns:
        uploaded_file: The uploaded resume file
    """
    st.title("AI Resume Parser")
    st.write("Upload a resume to extract information using Cohere AI")
    
    uploaded_file = st.file_uploader(
        "Choose a resume file", 
        type=["pdf", "docx", "txt"],
        help="Upload a resume in PDF, DOCX, or TXT format"
    )
    
    if 'parse_clicked' not in st.session_state:
        st.session_state.parse_clicked = False
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Parse Resume", disabled=uploaded_file is None):
            st.session_state.parse_clicked = True
    
    with col2:
        if st.button("Reset"):
            st.session_state.parse_clicked = False
            for key in list(st.session_state.keys()):
                if key != 'parse_clicked':
                    del st.session_state[key]
            st.experimental_rerun()
    
    if uploaded_file is not None:
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        
        st.write("**File Details:**")
        for key, value in file_details.items():
            st.write(f"- {key}: {value}")
    
    return uploaded_file