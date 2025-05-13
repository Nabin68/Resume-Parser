import os
import json
import cohere
import streamlit as st

def parse_resume(cleaned_text):
    """
    Parse the resume text using the Cohere API to extract structured information.
    
    Args:
        cleaned_text (str): The preprocessed resume text
        
    Returns:
        dict: A dictionary containing the parsed resume information
    """
    # Get the API key from environment variables
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY not found in environment variables")
    
    # Initialize the Cohere client
    co = cohere.Client(api_key)
    
    # Create the prompt for Cohere
    prompt = create_cohere_prompt(cleaned_text)
    
    try:
        # Call the Cohere Generate API
        response = co.generate(
            prompt=prompt,
            max_tokens=2500,
            temperature=0.1,  # Low temperature for more focused extraction
            k=0,
            p=0.75,
            stop_sequences=["---"],
            return_likelihoods='NONE'
        )
        
        # Extract the generated text
        generated_text = response.generations[0].text
        
        # Parse the JSON from the response
        # We need to find where the JSON starts and ends
        try:
            # Try to find JSON-formatted content
            start_idx = generated_text.find('{')
            end_idx = generated_text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = generated_text[start_idx:end_idx]
                parsed_data = json.loads(json_str)
            else:
                # If no JSON found, create a fallback structure
                st.warning("Structured JSON not found in the API response. Using best-effort parsing.")
                parsed_data = fallback_parser(generated_text)
                
            return parsed_data
            
        except json.JSONDecodeError:
            # If JSON parsing fails, use a fallback parser
            st.warning("Failed to parse JSON from the API response. Using best-effort parsing.")
            return fallback_parser(generated_text)
            
    except Exception as e:
        st.error(f"Error communicating with Cohere API: {str(e)}")
        raise
        
def create_cohere_prompt(resume_text):
    """
    Create a prompt for the Cohere API to extract resume information.
    
    Args:
        resume_text (str): The preprocessed resume text
        
    Returns:
        str: The prompt for the Cohere API
    """
    prompt = f"""
    You are an expert resume parser. I will provide you with the text of a resume, and your task is to extract key information and organize it into a structured JSON format.

    Here's the resume text:
    ```
    {resume_text}
    ```

    Please extract the following information and format it exactly as a JSON object with these fields:
    1. full_name: The candidate's full name
    2. contact_info: 
       - email: Email address
       - phone: Phone number
       - linkedin: LinkedIn profile (if available)
       - location: Geographic location (if available)
    3. education: An array of education entries, each with:
       - degree: Degree obtained
       - institution: School/University name
       - date_range: Time period (start-end)
       - gpa: GPA (if available)
       - details: Additional details (if available)
    4. work_experience: An array of work experiences, each with:
       - title: Job title
       - company: Company name
       - date_range: Employment period
       - location: Job location (if available)
       - responsibilities: Array of key responsibilities/achievements
    5. skills: Array of skills grouped by category when possible (e.g., technical_skills, soft_skills, languages)
    6. certifications: Array of certifications (if available)
    7. projects: Array of projects (if available), each with title, description, and technologies used
    8. summary: Professional summary or objective statement (if available)

    Return ONLY the JSON object without any explanation or additional text. Ensure the JSON is valid and properly formatted.
    """
    
    return prompt

def fallback_parser(text):
    """
    A fallback parser to extract information if JSON parsing fails.
    
    Args:
        text (str): The text returned by the Cohere API
        
    Returns:
        dict: A dictionary with the parsed information
    """
    # Create a basic structure
    parsed_data = {
        "full_name": "",
        "contact_info": {
            "email": "",
            "phone": "",
            "linkedin": "",
            "location": ""
        },
        "education": [],
        "work_experience": [],
        "skills": [],
        "certifications": [],
        "projects": [],
        "summary": ""
    }
    
    # Try to extract sections from the text
    sections = text.split("\n\n")
    
    for section in sections:
        section = section.strip()
        
        # Try to identify what type of section this is and extract the data
        if "full_name" in section.lower():
            lines = section.split("\n")
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    if "name" in key.lower():
                        parsed_data["full_name"] = value.strip()
                        
        elif "contact" in section.lower() or "email" in section.lower():
            lines = section.split("\n")
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.lower().strip()
                    value = value.strip()
                    
                    if "email" in key:
                        parsed_data["contact_info"]["email"] = value
                    elif "phone" in key:
                        parsed_data["contact_info"]["phone"] = value
                    elif "linkedin" in key:
                        parsed_data["contact_info"]["linkedin"] = value
                    elif "location" in key:
                        parsed_data["contact_info"]["location"] = value
                        
        elif "education" in section.lower():
            # Extract education information
            education_entry = {
                "degree": "",
                "institution": "",
                "date_range": "",
                "gpa": "",
                "details": ""
            }
            
            lines = section.split("\n")
            for i, line in enumerate(lines):
                if i == 0:  # Skip the "EDUCATION" header
                    continue
                    
                line = line.strip()
                if not line:
                    continue
                    
                if i == 1:  # Assume this is degree + institution
                    parts = line.split(",", 1)
                    if len(parts) > 1:
                        education_entry["institution"] = parts[0].strip()
                        education_entry["degree"] = parts[1].strip()
                    else:
                        education_entry["institution"] = line
                elif "gpa" in line.lower():
                    education_entry["gpa"] = line
                elif any(month in line.lower() for month in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]):
                    education_entry["date_range"] = line
                else:
                    education_entry["details"] += line + " "
                    
            if education_entry["institution"]:
                parsed_data["education"].append(education_entry)
                
        elif "experience" in section.lower() or "work" in section.lower():
            # Extract work experience
            work_entry = {
                "title": "",
                "company": "",
                "date_range": "",
                "location": "",
                "responsibilities": []
            }
            
            lines = section.split("\n")
            for i, line in enumerate(lines):
                if i == 0:  # Skip the "EXPERIENCE" header
                    continue
                    
                line = line.strip()
                if not line:
                    continue
                    
                if i == 1:  # Assume this is job title + company
                    parts = line.split("at", 1)
                    if len(parts) > 1:
                        work_entry["title"] = parts[0].strip()
                        work_entry["company"] = parts[1].strip()
                    else:
                        work_entry["title"] = line
                elif any(month in line.lower() for month in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]):
                    work_entry["date_range"] = line
                elif line.startswith(("*", "-", "•")):
                    work_entry["responsibilities"].append(line.lstrip("*- •").strip())
                    
            if work_entry["title"] or work_entry["company"]:
                parsed_data["work_experience"].append(work_entry)
                
        elif "skill" in section.lower():
            # Extract skills
            lines = section.split("\n")
            for i, line in enumerate(lines):
                if i == 0:  # Skip the "SKILLS" header
                    continue
                    
                line = line.strip()
                if not line:
                    continue
                    
                if ":" in line:
                    # This is likely a skill category
                    category, skills = line.split(":", 1)
                    skills_list = [s.strip() for s in skills.split(",")]
                    parsed_data["skills"].extend(skills_list)
                else:
                    # Individual skill or list of skills
                    skills_list = [s.strip() for s in line.split(",")]
                    parsed_data["skills"].extend(skills_list)
                    
        elif "summary" in section.lower() or "objective" in section.lower():
            # Extract summary
            lines = section.split("\n")
            for i, line in enumerate(lines):
                if i == 0:  # Skip the header
                    continue
                    
                line = line.strip()
                if line:
                    parsed_data["summary"] += line + " "
                    
    # Clean up any empty strings
    parsed_data["summary"] = parsed_data["summary"].strip()
    
    return parsed_data