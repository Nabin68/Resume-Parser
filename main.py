"""
Result Display Module for Resume Parser
Displays parsed resume data in a clean, readable format.
"""
import tkinter as tk
from tkinter import ttk
import webbrowser
from datetime import datetime

class ResultDisplay:
    """A class for displaying parsed resume data in a nice format."""
    
    def __init__(self, parent_frame):
        """
        Initialize the result display.
        
        Args:
            parent_frame (tk.Frame): Parent frame to display results in
        """
        self.parent_frame = parent_frame
        self.result_widgets = []
        
        # Define colors for styling
        self.primary_color = "#3498db"  # Blue
        self.secondary_color = "#2c3e50"  # Dark blue
        self.background_color = "#ecf0f1"  # Light gray
        self.highlight_color = "#e74c3c"  # Red
        self.text_color = "#2c3e50"  # Dark blue
        self.section_bg_color = "#f9f9f9"  # Slightly off-white for sections
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.configure("Section.TFrame", background=self.section_bg_color)
        self.style.configure("BoldText.TLabel", font=("Helvetica", 11, "bold"))
        self.style.configure("SectionHeader.TLabel", 
                            font=("Helvetica", 12, "bold"),
                            foreground=self.primary_color)
        self.style.configure("Name.TLabel", 
                            font=("Helvetica", 18, "bold"),
                            foreground=self.secondary_color)
    
    def display_results(self, resume_data):
        """
        Display the parsed resume data.
        
        Args:
            resume_data (dict): Parsed resume data
        """
        # Clear previous results
        self._clear_previous_results()
        
        # Create main scrollable frame
        self.canvas = tk.Canvas(self.parent_frame, bg=self.background_color)
        self.scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="TFrame")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Store reference to widgets for later removal
        self.result_widgets.extend([self.canvas, self.scrollbar])
        
        # Display resume sections
        self._display_header_section(resume_data)
        self._display_summary_section(resume_data)
        self._display_skills_section(resume_data)
        self._display_experience_section(resume_data)
        self._display_education_section(resume_data)
        self._display_additional_sections(resume_data)
        
        # Add padding at the bottom
        ttk.Frame(self.scrollable_frame, height=20).pack(fill="x")
    
    def _clear_previous_results(self):
        """Clear any previous results displayed."""
        for widget in self.result_widgets:
            widget.destroy()
        self.result_widgets = []
    
    def _display_header_section(self, resume_data):
        """
        Display the header section with name and contact info.
        
        Args:
            resume_data (dict): Parsed resume data
        """
        # Create header frame
        header_frame = ttk.Frame(self.scrollable_frame, style="Section.TFrame")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Display name
        name_label = ttk.Label(header_frame, 
                              text=resume_data.get('full_name', 'Unknown Name'),
                              style="Name.TLabel")
        name_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Create contact info frame
        contact_frame = ttk.Frame(header_frame)
        contact_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Get contact info
        contact_info = resume_data.get('contact_info', {})
        
        # Display contact details
        if contact_info.get('email'):
            self._create_contact_item(contact_frame, "✉️", contact_info['email'], "mailto:")
        
        if contact_info.get('phone'):
            self._create_contact_item(contact_frame, "📱", contact_info['phone'], "tel:")
        
        if contact_info.get('location'):
            self._create_contact_item(contact_frame, "📍", contact_info['location'])
        
        if contact_info.get('linkedin'):
            self._create_contact_item(contact_frame, "🔗", "LinkedIn", url=contact_info['linkedin'])
        
        if contact_info.get('portfolio'):
            self._create_contact_item(contact_frame, "🌐", "Portfolio", url=contact_info['portfolio'])
    
    def _create_contact_item(self, parent, icon, text, url_prefix=None, url=None):
        """
        Create a contact item with icon and text/link.
        
        Args:
            parent (tk.Frame): Parent frame
            icon (str): Emoji or icon character
            text (str): Text to display
            url_prefix (str, optional): URL prefix for simple links
            url (str, optional): Full URL for complex links
        """
        frame = ttk.Frame(parent)
        frame.pack(side="left", padx=(0, 15), pady=2)
        
        # Icon
        icon_label = ttk.Label(frame, text=icon, font=("Helvetica", 11))
        icon_label.pack(side="left", padx=(0, 5))
        
        # Create clickable link if URL is provided
        if url_prefix or url:
            full_url = url if url else f"{url_prefix}{text}"
            link = ttk.Label(frame, 
                           text=text, 
                           foreground=self.primary_color,
                           font=("Helvetica", 11, "underline"),
                           cursor="hand2")
            link.pack(side="left")
            link.bind("<Button-1>", lambda e: webbrowser.open(full_url))
        else:
            # Regular text
            text_label = ttk.Label(frame, text=text, font=("Helvetica", 11))
            text_label.pack(side="left")
    
    def _display_summary_section(self, resume_data):
        """
        Display the professional summary section.
        
        Args:
            resume_data (dict): Parsed resume data
        """
        summary = resume_data.get('summary')
        if summary:
            # Create section
            section_frame = self._create_section_frame("Professional Summary")
            
            # Summary text
            summary_text = tk.Text(section_frame, 
                                  wrap="word", 
                                  height=4, 
                                  bg=self.section_bg_color,
                                  relief="flat",
                                  font=("Helvetica", 10))
            summary_text.insert("1.0", summary)
            summary_text.configure(state="disabled")  # Make read-only
            summary_text.pack(fill="x", padx=10, pady=5)
    
    def _display_skills_section(self, resume_data):
        """
        Display the skills section.
        
        Args:
            resume_data (dict): Parsed resume data
        """
        skills = resume_data.get('skills', {})
        technical_skills = skills.get('technical', [])
        soft_skills = skills.get('soft', [])
        
        if technical_skills or soft_skills:
            # Create section
            section_frame = self._create_section_frame("Skills")
            
            # Create two columns if both skill types exist
            if technical_skills and soft_skills:
                skills_frame = ttk.Frame(section_frame)
                skills_frame.pack(fill="x", padx=10, pady=5)
                
                # Technical skills column
                tech_frame = ttk.Frame(skills_frame)
                tech_frame.pack(side="left", fill="both", expand=True)
                
                ttk.Label(tech_frame, 
                         text="Technical Skills", 
                         style="BoldText.TLabel").pack(anchor="w", pady=(0, 5))
                
                self._create_skills_list(tech_frame, technical_skills)
                
                # Soft skills column
                soft_frame = ttk.Frame(skills_frame)
                soft_frame.pack(side="right", fill="both", expand=True)
                
                ttk.Label(soft_frame, 
                         text="Soft Skills", 
                         style="BoldText.TLabel").pack(anchor="w", pady=(0, 5))
                
                self._create_skills_list(soft_frame, soft_skills)
            else:
                # Single column for all skills
                skills_to_display = technical_skills or soft_skills
                self._create_skills_list(section_frame, skills_to_display)
    
    def _create_skills_list(self, parent, skills):
        """
        Create a visual list of skills.
        
        Args:
            parent (tk.Frame): Parent frame
            skills (list): List of skills to display
        """
        if not skills:
            return
        
        # Create a frame for the skills
        skills_frame = ttk.Frame(parent)
        skills_frame.pack(fill="x", pady=(0, 5))
        
        # Add each skill as a styled label
        row_frame = ttk.Frame(skills_frame)
        row_frame.pack(fill="x", pady=2)
        
        col_count = 0
        max_cols = 3  # Maximum number of skills per row
        
        for skill in skills:
            if col_count >= max_cols:
                # Create a new row
                row_frame = ttk.Frame(skills_frame)
                row_frame.pack(fill="x", pady=2)
                col_count = 0
            
            # Create skill chip/badge
            skill_frame = ttk.Frame(row_frame, padding=5)
            skill_frame.pack(side="left", padx=5, pady=2)
            
            skill_label = ttk.Label(skill_frame, 
                                   text=skill, 
                                   background=self.primary_color,
                                   foreground="white",
                                   padding=(5, 2))
            skill_label.pack()
            
            col_count += 1
    
    def _display_experience_section(self, resume_data):
        """
        Display the work experience section.
        
        Args:
            resume_data (dict): Parsed resume data
        """
        experience_entries = resume_data.get('work_experience', [])
        
        if experience_entries:
            # Create section
            section_frame = self._create_section_frame("Work Experience")
            
            # Add each experience entry
            for entry in experience_entries:
                self._create_experience_entry(section_frame, entry)
    
    def _create_experience_entry(self, parent, experience):
        """
        Create a single work experience entry.
        
        Args:
            parent (tk.Frame): Parent frame
            experience (dict): Experience entry data
        """
        # Create entry frame
        entry_frame = ttk.Frame(parent, style="TFrame")
        entry_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        # Add separator above entries (except the first one)
        if entry_frame.winfo_children():
            separator = ttk.Separator(entry_frame, orient="horizontal")
            separator.pack(fill="x", pady=(0, 10))
        
        # Header row with job title and date range
        header_frame = ttk.Frame(entry_frame)
        header_frame.pack(fill="x", pady=(5, 0))
        
        # Job title
        job_title = experience.get('job_title', '')
        job_label = ttk.Label(header_frame, 
                             text=job_title, 
                             style="BoldText.TLabel")
        job_label.pack(side="left")
        
        # Date range (right-aligned)
        date_range = experience.get('date_range', '')
        if date_range:
            date_label = ttk.Label(header_frame, text=date_range)
            date_label.pack(side="right")
        
        # Company and location
        company_frame = ttk.Frame(entry_frame)
        company_frame.pack(fill="x", pady=(0, 5), anchor="w")
        
        company = experience.get('company', '')
        company_label = ttk.Label(company_frame, 
                                text=company, 
                                font=("Helvetica", 10, "italic"))
        company_label.pack(side="left")
        
        # Location (if available)
        location = experience.get('location', '')
        if location:
            location_label = ttk.Label(company_frame, 
                                     text=f" | {location}", 
                                     font=("Helvetica", 10, "italic"))
            location_label.pack(side="left")
        
        # Description
        description = experience.get('description', '')
        if description:
            desc_text = tk.Text(entry_frame, 
                              wrap="word", 
                              height=4, 
                              bg=self.section_bg_color,
                              relief="flat",
                              font=("Helvetica", 10))
            desc_text.insert("1.0", description)
            desc_text.configure(state="disabled")  # Make read-only
            desc_text.pack(fill="x", pady=(5, 0))
    
    def _display_education_section(self, resume_data):
        """
        Display the education section.
        
        Args:
            resume_data (dict): Parsed resume data
        """
        education_entries = resume_data.get('education', [])
        
        if education_entries:
            # Create section
            section_frame = self._create_section_frame("Education")
            
            # Add each education entry
            for entry in education_entries:
                self._create_education_entry(section_frame, entry)
    
    def _create_education_entry(self, parent, education):
        """
        Create a single education entry.
        
        Args:
            parent (tk.Frame): Parent frame
            education (dict): Education entry data
        """
        # Create entry frame
        entry_frame = ttk.Frame(parent, style="TFrame")
        entry_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Degree and graduation date
        header_frame = ttk.Frame(entry_frame)
        header_frame.pack(fill="x")
        
        # Degree and field
        degree = education.get('degree', '')
        field = education.get('field_of_study', '')
        
        degree_text = f"{degree}{', ' + field if field else ''}"
        degree_label = ttk.Label(header_frame, 
                               text=degree_text, 
                               style="BoldText.TLabel")
        degree_label.pack(side="left")
        
        # Graduation date
        grad_date = education.get('graduation_date', '')
        if grad_date:
            date_label = ttk.Label(header_frame, text=grad_date)
            date_label.pack(side="right")
        
        # Institution
        institution = education.get('institution', '')
        if institution:
            institution_label = ttk.Label(entry_frame, 
                                        text=institution, 
                                        font=("Helvetica", 10, "italic"))
            institution_label.pack(anchor="w")
    
    def _display_additional_sections(self, resume_data):
        """
        Display additional sections like certifications, projects, etc.
        
        Args:
            resume_data (dict): Parsed resume data
        """
        # Certifications
        certifications = resume_data.get('certifications', [])
        if certifications:
            cert_frame = self._create_section_frame("Certifications")
            
            for cert in certifications:
                cert_label = ttk.Label(cert_frame, text=f"• {cert}", padding=(10, 2))
                cert_label.pack(anchor="w")
        
        # Projects
        projects = resume_data.get('projects', [])
        if projects:
            proj_frame = self._create_section_frame("Projects")
            
            for project in projects:
                self._create_project_entry(proj_frame, project)
        
        # Languages
        languages = resume_data.get('languages', [])
        if languages:
            lang_frame = self._create_section_frame("Languages")
            
            lang_text = ", ".join(languages)
            lang_label = ttk.Label(lang_frame, text=lang_text, padding=(10, 5))
            lang_label.pack(anchor="w")
        
        # Interests
        interests = resume_data.get('interests', [])
        if interests:
            interest_frame = self._create_section_frame("Interests")
            
            interest_text = ", ".join(interests)
            interest_label = ttk.Label(interest_frame, text=interest_text, padding=(10, 5))
            interest_label.pack(anchor="w")
    
    def _create_project_entry(self, parent, project):
        """
        Create a single project entry.
        
        Args:
            parent (tk.Frame): Parent frame
            project (dict): Project entry data
        """
        # Project frame
        project_frame = ttk.Frame(parent)
        project_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Project name
        name = project.get('name', '')
        if name:
            name_label = ttk.Label(project_frame, 
                                 text=name, 
                                 style="BoldText.TLabel")
            name_label.pack(anchor="w")
        
        # Technologies used
        techs = project.get('technologies', [])
        if techs:
            tech_frame = ttk.Frame(project_frame)
            tech_frame.pack(fill="x", anchor="w", pady=(0, 5))
            
            tech_label = ttk.Label(tech_frame, 
                                 text="Technologies: ", 
                                 font=("Helvetica", 9, "italic"))
            tech_label.pack(side="left")
            
            tech_value = ttk.Label(tech_frame, 
                                 text=", ".join(techs))
            tech_value.pack(side="left")
        
        # Description
        description = project.get('description', '')
        if description:
            desc_label = ttk.Label(project_frame, 
                                 text=description, 
                                 wraplength=500)
            desc_label.pack(anchor="w")
    
    def _create_section_frame(self, title):
        """
        Create a section frame with title.
        
        Args:
            title (str): Section title
            
        Returns:
            ttk.Frame: The created section frame
        """
        # Create outer frame with padding
        outer_frame = ttk.Frame(self.scrollable_frame)
        outer_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Section title
        section_title = ttk.Label(outer_frame, 
                                text=title, 
                                style="SectionHeader.TLabel")
        section_title.pack(anchor="w", padx=5)
        
        # Section divider
        divider = ttk.Separator(outer_frame, orient="horizontal")
        divider.pack(fill="x", padx=5, pady=(0, 5))
        
        # Content frame
        content_frame = ttk.Frame(outer_frame, style="Section.TFrame")
        content_frame.pack(fill="x", padx=5)
        
        return content_frame