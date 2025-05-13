import json
import pandas as pd
import streamlit as st
import io

def export_data(parsed_data):
    """
    Allow exporting of the parsed resume data in various formats.
    
    Args:
        parsed_data (dict): The parsed resume information
    """
    st.subheader("Export Data")
    
    # Create columns for export buttons
    col1, col2, col3 = st.columns(3)
    
    # JSON export
    with col1:
        json_data = json.dumps(parsed_data, indent=2)
        json_bytes = json_data.encode('utf-8')
        
        st.download_button(
            label="📥 Download JSON",
            data=json_bytes,
            file_name=f"{parsed_data.get('full_name', 'resume').replace(' ', '_').lower()}_parsed.json",
            mime="application/json"
        )
    
    # CSV export
    with col2:
        # Convert the nested dictionary to a flat CSV-friendly format
        flat_data = flatten_data(parsed_data)
        
        # Create a DataFrame and convert to CSV
        df = pd.DataFrame([flat_data])
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{parsed_data.get('full_name', 'resume').replace(' ', '_').lower()}_parsed.csv",
            mime="text/csv"
        )
    
    # Text export
    with col3:
        # Create a readable text format
        text_data = format_text(parsed_data)
        
        st.download_button(
            label="📥 Download Text",
            data=text_data,
            file_name=f"{parsed_data.get('full_name', 'resume').replace(' ', '_').lower()}_parsed.txt",
            mime="text/plain"
        )

def flatten_data(parsed_data):
    """
    Flatten the nested dictionary to a format suitable for CSV export.
    
    Args:
        parsed_data (dict): The parsed resume information
        
    Returns:
        dict: Flattened data ready for CSV export
    """
    flat_data = {}
    
    # Personal information
    flat_data['full_name'] = parsed_data.get('full_name', '')
    
    # Contact information
    contact_info = parsed_data.get('contact_info', {})
    flat_data['email'] = contact_info.get('email', '')
    flat_data['phone'] = contact_info.get('phone', '')
    flat_data['linkedin'] = contact_info.get('linkedin', '')
    flat_data['location'] = contact_info.get('location', '')
    
    # Summary
    flat_data['summary'] = parsed_data.get('summary', '')
    
    # Education
    education_list = parsed_data.get('education', [])
    for i, edu in enumerate(education_list[:3]):  # Limit to 3 for simplicity
        prefix = f'education_{i+1}'
        flat_data[f'{prefix}_institution'] = edu.get('institution', '')
        flat_data[f'{prefix}_degree'] = edu.get('degree', '')
        flat_data[f'{prefix}_date_range'] = edu.get('date_range', '')
        flat_data[f'{prefix}_gpa'] = edu.get('gpa', '')
    
    # Work experience
    work_list = parsed_data.get('work_experience', [])
    for i, work in enumerate(work_list[:3]):  # Limit to 3 for simplicity
        prefix = f'experience_{i+1}'
        flat_data[f'{prefix}_title'] = work.get('title', '')
        flat_data[f'{prefix}_company'] = work.get('company', '')
        flat_data[f'{prefix}_date_range'] = work.get('date_range', '')
        flat_data[f'{prefix}_location'] = work.get('location', '')
        
        # Responsibilities as a comma-separated string
        responsibilities = work.get('responsibilities', [])
        flat_data[f'{prefix}_responsibilities'] = ', '.join(responsibilities)
    
    # Skills
    skills = parsed_data.get('skills', [])
    if isinstance(skills, dict):
        # Categorized skills
        for category, skill_list in skills.items():
            flat_data[f'skills_{category}'] = ', '.join(skill_list)
    else:
        # Flat list of skills
        flat_data['skills'] = ', '.join(skills)
    
    return flat_data

def format_text(parsed_data):
    """
    Format the parsed resume data as a readable text document.
    
    Args:
        parsed_data (dict): The parsed resume information
        
    Returns:
        str: Formatted text
    """
    text = []
    
    # Personal information
    text.append(f"Name: {parsed_data.get('full_name', 'N/A')}")
    
    # Contact information
    contact_info = parsed_data.get('contact_info', {})
    text.append("\nCONTACT INFORMATION:")
    text.append(f"Email: {contact_info.get('email', 'N/A')}")
    text.append(f"Phone: {contact_info.get('phone', 'N/A')}")
    
    if contact_info.get('linkedin'):
        text.append(f"LinkedIn: {contact_info.get('linkedin')}")
        
    if contact_info.get('location'):
        text.append(f"Location: {contact_info.get('location')}")
    
    # Summary
    if parsed_data.get('summary'):
        text.append("\nPROFESSIONAL SUMMARY:")
        text.append(parsed_data.get('summary'))
    
    # Education
    education_list = parsed_data.get('education', [])
    if education_list:
        text.append("\nEDUCATION:")
        for edu in education_list:
            text.append(f"- {edu.get('institution', 'N/A')}")
            text.append(f"  Degree: {edu.get('degree', 'N/A')}")
            
            if edu.get('date_range'):
                text.append(f"  Period: {edu.get('date_range')}")
                
            if edu.get('gpa'):
                text.append(f"  GPA: {edu.get('gpa')}")
                
            if edu.get('details'):
                text.append(f"  Details: {edu.get('details')}")
                
            text.append("")  # Empty line between entries
    
    # Work experience
    work_list = parsed_data.get('work_experience', [])
    if work_list:
        text.append("\nWORK EXPERIENCE:")
        for work in work_list:
            text.append(f"- {work.get('title', 'N/A')} at {work.get('company', 'N/A')}")
            
            if work.get('date_range'):
                text.append(f"  Period: {work.get('date_range')}")
                
            if work.get('location'):
                text.append(f"  Location: {work.get('location')}")
            
            # Responsibilities
            responsibilities = work.get('responsibilities', [])
            if responsibilities:
                text.append("  Responsibilities/Achievements:")
                for resp in responsibilities:
                    text.append(f"  * {resp}")
            
            text.append("")  # Empty line between entries
    
    # Skills
    skills = parsed_data.get('skills', [])
    if skills:
        text.append("\nSKILLS:")
        if isinstance(skills, dict):
            # Categorized skills
            for category, skill_list in skills.items():
                text.append(f"- {category.title()}: {', '.join(skill_list)}")
        else:
            # Flat list of skills
            text.append(f"- {', '.join(skills)}")
    
    # Projects
    projects = parsed_data.get('projects', [])
    if projects:
        text.append("\nPROJECTS:")
        for project in projects:
            if isinstance(project, dict):
                text.append(f"- {project.get('title', 'N/A')}")
                text.append(f"  Description: {project.get('description', 'N/A')}")
                
                if project.get('technologies'):
                    text.append(f"  Technologies: {', '.join(project.get('technologies', []))}")
            else:
                text.append(f"- {project}")
            
            text.append("")  # Empty line between entries
    
    # Certifications
    certifications = parsed_data.get('certifications', [])
    if certifications:
        text.append("\nCERTIFICATIONS:")
        for cert in certifications:
            if isinstance(cert, dict):
                text.append(f"- {cert.get('name', 'N/A')}")
                
                if cert.get('issuer'):
                    text.append(f"  Issuer: {cert.get('issuer')}")
                    
                if cert.get('date'):
                    text.append(f"  Date: {cert.get('date')}")
            else:
                text.append(f"- {cert}")
            
            text.append("")  # Empty line between entries
    
    return '\n'.join(text)