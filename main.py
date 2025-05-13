import os
import streamlit as st
from dotenv import load_dotenv

from gui.interface import create_interface
from reader.file_reader import read_resume
from preprocessor.cleaner import clean_text
from parser.cohere_parser import parse_resume
from display.result_display import display_results
from exporter.save import export_data

load_dotenv()

if not os.getenv("COHERE_API_KEY"):
    st.error("Please set your COHERE_API_KEY in the .env file")
    st.stop()

def main():
    # Set up page configuration
    st.set_page_config(
        page_title="Resume Parser",
        page_icon="📄",
        layout="wide"
    )
    
    uploaded_file = create_interface()
    
    if uploaded_file is not None and st.session_state.get('parse_clicked', False):
        with st.spinner("Processing resume..."):
            try:
                raw_text = read_resume(uploaded_file)
                
                cleaned_text = clean_text(raw_text)
                
                parsed_data = parse_resume(cleaned_text)
                
                display_results(parsed_data)
                
                export_data(parsed_data)
                
            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")
                
if __name__ == "__main__":
    main()