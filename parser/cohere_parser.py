"""
Cohere API Parser Module for Resume Parser
Handles interaction with the Cohere Generate API for resume parsing.
"""
import os
import json
import cohere
from dotenv import load_dotenv

class CohereParser:
    """A class for parsing resumes using the Cohere API."""
    
    def __init__(self):
        """Initialize the Cohere parser with API key from environment variables."""
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment
        self.api_key = os.getenv('COHERE_API_KEY')
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not found")
        
        # Initialize Cohere client
        self.client = cohere.Client(self.api_key)
    
    def parse_resume(self, text):
        """
        Parse resume text using Cohere API.
        
        Args:
            text (str): Cleaned resume text to parse
            
        Returns:
            dict: Structured resume data
        """
        try:
            # Craft the prompt for Cohere API
            prompt = self._create_parsing_prompt(text)
            
            # Call Cohere Generate API
            response = self.client.generate(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.2,  # Lower temperature for more deterministic output
                k=0,
                p=0.75,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                stop_sequences=["```"],
                return_likelihoods="NONE"
            )
            
            # Extract and parse JSON from response
            parsed_data = self._extract_json_from_response(response)
            return parsed_data
            
        except Exception as e:
            raise Exception(f"Error parsing resume with Cohere API: {str(e)}")
    
    def _create_parsing_prompt(self, text):
        """
        Create a prompt for Cohere API to parse resume.
        
        Args:
            text (str): Resume text to parse
            
        Returns:
            str: Complete prompt for Cohere API
        """
        # Create a detailed prompt that instructs the model how to parse the resume
        prompt = f"""As an expert resume analyzer, extract structured information from the resume below. 
Identify and organize the following sections:

1. Full Name
2. Contact Information (Email, Phone Number, Location, LinkedIn/Portfolio URLs)
3. Professional Summary
4. Skills (both technical and soft skills)
5. Work Experience (for each position: company name, job title, dates, location, and key responsibilities/achievements)
6. Education (for each entry: institution, degree, field of study, graduation date)
7. Certifications/Additional Training
8. Projects (if any)
9. Languages (if any)
10. Interests/Hobbies (if present)

Format the extraction as a valid JSON object with clear organization.

Resume text:
```
{text}
```

Return the extracted information in the following JSON format:
```json
{{
  "full_name": "",
  "contact_info": {{
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "portfolio": ""
  }},
  "summary": "",
  "skills": {{
    "technical": [],
    "soft": []
  }},
  "work_experience": [
    {{
      "company": "",
      "job_title": "",
      "date_range": "",
      "location": "",
      "description": ""
    }}
  ],
  "education": [
    {{
      "institution": "",
      "degree": "",
      "field_of_study": "",
      "graduation_date": ""
    }}
  ],
  "certifications": [],
  "projects": [
    {{
      "name": "",
      "description": "",
      "technologies": []
    }}
  ],
  "languages": [],
  "interests": []
}}
```
Ensure that all JSON fields are properly formatted and escaped. Leave fields empty if the information isn't available in the resume.
"""
        return prompt
    
    def _extract_json_from_response(self, response):
        """
        Extract and parse JSON from Cohere API response.
        
        Args:
            response: Cohere API response
            
        Returns:
            dict: Parsed JSON data
        """
        try:
            # Extract the text from the response
            generated_text = response.generations[0].text
            
            # Find JSON content between ```json and ``` markers if present
            json_pattern = r'```json\s*([\s\S]*?)\s*```'
            import re
            json_match = re.search(json_pattern, generated_text)
            
            if json_match:
                json_str = json_match.group(1)
            else:
                # If no markers, assume the entire text is JSON
                json_str = generated_text
            
            # Clean up any remaining markdown or non-JSON content
            json_str = json_str.strip()
            
            # Parse the JSON
            parsed_data = json.loads(json_str)
            
            # Validate the structure
            self._validate_parsed_data(parsed_data)
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from API response: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing API response: {str(e)}")
    
    def _validate_parsed_data(self, data):
        """
        Validate the structure of parsed resume data.
        
        Args:
            data (dict): Parsed resume data to validate
            
        Returns:
            bool: True if valid, raises exception otherwise
        """
        # Required top-level keys
        required_keys = [
            'full_name', 
            'contact_info', 
            'skills', 
            'work_experience', 
            'education'
        ]
        
        # Check for required keys
        for key in required_keys:
            if key not in data:
                data[key] = "" if key in ['full_name'] else {} if key in ['contact_info', 'skills'] else []
        
        # Ensure contact_info structure
        if 'contact_info' in data and not isinstance(data['contact_info'], dict):
            data['contact_info'] = {}
        
        # Ensure skills structure
        if 'skills' in data and not isinstance(data['skills'], dict):
            if isinstance(data['skills'], list):
                data['skills'] = {
                    'technical': data['skills'],
                    'soft': []
                }
            else:
                data['skills'] = {
                    'technical': [],
                    'soft': []
                }
        
        # Convert any None values to empty strings, lists, or dicts
        for key in data:
            if data[key] is None:
                if key in ['full_name', 'summary']:
                    data[key] = ""
                elif key in ['work_experience', 'education', 'certifications', 'projects', 'languages', 'interests']:
                    data[key] = []
                elif key in ['contact_info', 'skills']:
                    data[key] = {}
        
        return True