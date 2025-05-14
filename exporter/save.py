"""
Export module for the Resume Parser application.
Handles saving parsed resume data to various formats.
"""

import os
import json
import csv
import datetime
from typing import Dict, Any, Optional


class ResumeExporter:
    """Class for exporting parsed resume data to different file formats."""

    def __init__(self, output_dir: str = "exports"):
        """
        Initialize the ResumeExporter.
        
        Args:
            output_dir: Directory to save exported files (default: "exports")
        """
        self.output_dir = output_dir
        self._ensure_export_dir_exists()
    
    def _ensure_export_dir_exists(self) -> None:
        """Create the export directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _generate_filename(self, candidate_name: str, extension: str) -> str:
        """
        Generate a filename based on candidate name and current timestamp.
        
        Args:
            candidate_name: Name of the candidate from the resume
            extension: File extension for the export format (without dot)
            
        Returns:
            Formatted filename string
        """
        # Clean the candidate name for use in a filename
        clean_name = "".join(c if c.isalnum() else "_" for c in candidate_name)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{clean_name}_{timestamp}.{extension}"
    
    def save_json(self, resume_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save resume data as JSON file.
        
        Args:
            resume_data: Dictionary containing parsed resume information
            filename: Optional custom filename (default: auto-generated)
            
        Returns:
            Path to the saved file
        """
        if not filename:
            candidate_name = resume_data.get("full_name", "candidate")
            filename = self._generate_filename(candidate_name, "json")
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as json_file:
            json.dump(resume_data, json_file, indent=4)
        
        return filepath
    
    def save_csv(self, resume_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save resume data as CSV file.
        Note: This flattens nested structures to fit in CSV format.
        
        Args:
            resume_data: Dictionary containing parsed resume information
            filename: Optional custom filename (default: auto-generated)
            
        Returns:
            Path to the saved file
        """
        if not filename:
            candidate_name = resume_data.get("full_name", "candidate")
            filename = self._generate_filename(candidate_name, "csv")
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Flatten nested structures for CSV format
        flattened_data = self._flatten_resume_data(resume_data)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(flattened_data.keys())
            writer.writerow(flattened_data.values())
        
        return filepath
    
    def _flatten_resume_data(self, resume_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Convert nested resume data structure to flat dictionary for CSV export.
        
        Args:
            resume_data: Dictionary containing parsed resume information
            
        Returns:
            Flattened dictionary with string values
        """
        flattened = {}
        
        # Basic fields
        flattened["full_name"] = resume_data.get("full_name", "")
        flattened["email"] = resume_data.get("email", "")
        flattened["phone"] = resume_data.get("phone", "")
        
        # Skills (convert list to comma-separated string)
        if "skills" in resume_data and isinstance(resume_data["skills"], list):
            flattened["skills"] = ", ".join(resume_data["skills"])
        else:
            flattened["skills"] = str(resume_data.get("skills", ""))
        
        # Education (summarize into single field)
        if "education" in resume_data and isinstance(resume_data["education"], list):
            education_entries = []
            for edu in resume_data["education"]:
                if isinstance(edu, dict):
                    parts = []
                    if "degree" in edu:
                        parts.append(edu["degree"])
                    if "institution" in edu:
                        parts.append(f"at {edu['institution']}")
                    if "year" in edu:
                        parts.append(f"({edu['year']})")
                    education_entries.append(" ".join(parts))
                else:
                    education_entries.append(str(edu))
            flattened["education"] = " | ".join(education_entries)
        else:
            flattened["education"] = str(resume_data.get("education", ""))
        
        # Work Experience (summarize into single field)
        if "experience" in resume_data and isinstance(resume_data["experience"], list):
            experience_entries = []
            for exp in resume_data["experience"]:
                if isinstance(exp, dict):
                    parts = []
                    if "title" in exp:
                        parts.append(exp["title"])
                    if "company" in exp:
                        parts.append(f"at {exp['company']}")
                    if "duration" in exp:
                        parts.append(f"({exp['duration']})")
                    experience_entries.append(" ".join(parts))
                else:
                    experience_entries.append(str(exp))
            flattened["experience"] = " | ".join(experience_entries)
        else:
            flattened["experience"] = str(resume_data.get("experience", ""))
        
        # Projects/Certifications
        if "projects" in resume_data:
            if isinstance(resume_data["projects"], list):
                flattened["projects"] = " | ".join(str(proj) for proj in resume_data["projects"])
            else:
                flattened["projects"] = str(resume_data["projects"])
        
        if "certifications" in resume_data:
            if isinstance(resume_data["certifications"], list):
                flattened["certifications"] = " | ".join(str(cert) for cert in resume_data["certifications"])
            else:
                flattened["certifications"] = str(resume_data["certifications"])
        
        return flattened