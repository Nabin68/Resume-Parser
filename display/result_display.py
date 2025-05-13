import streamlit as st
import pandas as pd
import json

def display_results(parsed_data):
    """
    Display the parsed resume data in a user-friendly format.
    
    Args:
        parsed_data (dict): The parsed resume information
    """
    # Create a section for the parsed results
    st.header("Parsed Resume Information")
    
    # Personal Information
    with st.expander("📋 Personal Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Basic Details")
            st.write(f"**Name:** {parsed_data.get('full_name', 'N/A')}")
            
            # Contact information
            contact_info = parsed_data.get('contact_info', {})
            st.write(f"**Email:** {contact_info.get('email', 'N/A')}")
            st.write(f"**Phone:** {contact_info.get('phone', 'N/A')}")
            st.write(f"**Location:** {contact_info.get('location', 'N/A')}")
            
            if contact_info.get('linkedin'):
                st.write(f"**LinkedIn:** {contact_info.get('linkedin')}")
        
        with col2:
            # Professional Summary
            st.subheader("Professional Summary")
            summary = parsed_data.get('summary', 'No summary provided')
            st.write(summary)
    
    # Education
    with st.expander("🎓 Education", expanded=True):
        education_data = parsed_data.get('education', [])
        
        if not education_data:
            st.write("No education information found")
        else:
            for i, edu in enumerate(education_data):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(edu.get('institution', f"Institution {i+1}"))
                    st.write(f"**Degree:** {edu.get('degree', 'N/A')}")
                    
                    if edu.get('gpa'):
                        st.write(f"**GPA:** {edu.get('gpa')}")
                    
                    if edu.get('details'):
                        st.write(f"**Details:** {edu.get('details')}")
                
                with col2:
                    st.write(f"**Period:** {edu.get('date_range', 'N/A')}")
                
                if i < len(education_data) - 1:
                    st.divider()
    
    # Work Experience
    with st.expander("💼 Work Experience", expanded=True):
        work_experience = parsed_data.get('work_experience', [])
        
        if not work_experience:
            st.write("No work experience found")
        else:
            for i, exp in enumerate(work_experience):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"{exp.get('title', 'Position')} at {exp.get('company', 'Company')}")
                    
                    if exp.get('location'):
                        st.write(f"**Location:** {exp.get('location')}")
                
                with col2:
                    st.write(f"**Period:** {exp.get('date_range', 'N/A')}")
                
                # Responsibilities
                responsibilities = exp.get('responsibilities', [])
                if responsibilities:
                    st.write("**Responsibilities/Achievements:**")
                    for resp in responsibilities:
                        st.write(f"- {resp}")
                
                if i < len(work_experience) - 1:
                    st.divider()
    
    # Skills
    with st.expander("🔧 Skills", expanded=True):
        skills = parsed_data.get('skills', [])
        
        if not skills:
            st.write("No skills found")
        else:
            # Check if skills are already categorized
            if isinstance(skills, dict):
                # Skills are categorized
                for category, skill_list in skills.items():
                    st.subheader(category.title())
                    
                    # Convert to columns for better display
                    skills_per_row = 3
                    skills_rows = [skill_list[i:i+skills_per_row] for i in range(0, len(skill_list), skills_per_row)]
                    
                    for row in skills_rows:
                        cols = st.columns(skills_per_row)
                        for i, skill in enumerate(row):
                            cols[i].write(f"- {skill}")
            else:
                # Skills are a flat list
                st.subheader("Skills List")
                
                # Convert to columns for better display
                skills_per_row = 3
                skills_rows = [skills[i:i+skills_per_row] for i in range(0, len(skills), skills_per_row)]
                
                for row in skills_rows:
                    cols = st.columns(skills_per_row)
                    for i, skill in enumerate(row):
                        cols[i].write(f"- {skill}")
    
    # Projects
    if parsed_data.get('projects'):
        with st.expander("🚀 Projects", expanded=True):
            projects = parsed_data.get('projects', [])
            
            for i, project in enumerate(projects):
                if isinstance(project, dict):
                    st.subheader(project.get('title', f"Project {i+1}"))
                    st.write(project.get('description', 'No description available'))
                    
                    if project.get('technologies'):
                        st.write("**Technologies used:**")
                        st.write(", ".join(project.get('technologies', [])))
                else:
                    # If project is just a string
                    st.subheader(f"Project {i+1}")
                    st.write(project)
                
                if i < len(projects) - 1:
                    st.divider()
    
    # Certifications
    if parsed_data.get('certifications'):
        with st.expander("🏆 Certifications", expanded=True):
            certifications = parsed_data.get('certifications', [])
            
            if not certifications:
                st.write("No certifications found")
            else:
                for i, cert in enumerate(certifications):
                    if isinstance(cert, dict):
                        st.write(f"**{cert.get('name', f'Certification {i+1}')}**")
                        
                        if cert.get('issuer'):
                            st.write(f"Issuer: {cert.get('issuer')}")
                            
                        if cert.get('date'):
                            st.write(f"Date: {cert.get('date')}")
                    else:
                        # If certification is just a string
                        st.write(f"- {cert}")
    
    # Store the parsed data in session state for export
    st.session_state['parsed_data'] = parsed_data