"""
GUI module for the Resume Parser application.
Provides the user interface for uploading, parsing and viewing resumes.
"""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import re

class ResumeParserGUI:
    """GUI for the Resume Parser application using Tkinter."""
    
    def __init__(self, root, process_callback):
        """
        Initialize the GUI.
        
        Args:
            root (tk.Tk): The root Tkinter window
            process_callback (function): Callback function to process the resume
        """
        self.root = root
        self.process_callback = process_callback
        self.file_path = None
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface components."""
        # Define colors
        self.primary_color = "#3498db"  # Blue
        self.secondary_color = "#2c3e50"  # Dark blue
        self.background_color = "#ecf0f1"  # Light gray
        self.accent_color = "#e74c3c"  # Red
        self.text_color = "#2c3e50"  # Dark blue
        
        # Configure root window
        self.root.configure(bg=self.background_color)
        
        # Create a style for ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure ttk styles
        self.style.configure("TFrame", background=self.background_color)
        self.style.configure("TButton", 
                             background=self.primary_color, 
                             foreground="white", 
                             font=("Helvetica", 10, "bold"),
                             borderwidth=0)
        self.style.map("TButton", 
                       background=[("active", self.accent_color), 
                                   ("disabled", "#95a5a6")])
        self.style.configure("TLabel", 
                             background=self.background_color, 
                             foreground=self.text_color, 
                             font=("Helvetica", 10))
        self.style.configure("Header.TLabel", 
                             background=self.background_color, 
                             foreground=self.text_color, 
                             font=("Helvetica", 16, "bold"))
        self.style.configure("Subheader.TLabel", 
                             background=self.background_color, 
                             foreground=self.text_color, 
                             font=("Helvetica", 12, "bold"))
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title frame
        self.title_frame = ttk.Frame(self.main_frame)
        self.title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # App title
        self.title_label = ttk.Label(self.title_frame, 
                                    text="Resume Parser", 
                                    style="Header.TLabel",
                                    font=("Helvetica", 24, "bold"))
        self.title_label.pack(side=tk.LEFT)
        
        # Horizontal divider
        self.divider = ttk.Separator(self.main_frame, orient=tk.HORIZONTAL)
        self.divider.pack(fill=tk.X, pady=10)
        
        # Create a split view with PanedWindow
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (upload section)
        self.upload_frame = ttk.Frame(self.paned_window, padding=(0, 10))
        
        # Right panel (results section)
        self.results_frame = ttk.Frame(self.paned_window, padding=(10, 10))
        
        # Add frames to paned window
        self.paned_window.add(self.upload_frame, weight=1)
        self.paned_window.add(self.results_frame, weight=2)
        
        # Set up upload section
        self.setup_upload_section()
        
        # Set up results section placeholder
        self.setup_results_placeholder()
        
        # Status bar
        self.status_bar = ttk.Label(self.root, 
                                   text="Ready", 
                                   relief=tk.SUNKEN, 
                                   anchor=tk.W, 
                                   padding=(5, 2))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_upload_section(self):
        """Set up the upload section of the GUI."""
        # Upload frame header
        self.upload_header = ttk.Label(self.upload_frame, 
                                      text="Upload Resume", 
                                      style="Subheader.TLabel")
        self.upload_header.pack(pady=(0, 10), anchor=tk.W)
        
        # File upload area
        self.upload_area = ttk.Frame(self.upload_frame, 
                                    style="TFrame", 
                                    borderwidth=2, 
                                    relief=tk.GROOVE)
        self.upload_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Upload icon (you could replace this with an actual icon)
        self.upload_icon_label = ttk.Label(self.upload_area, 
                                         text="📄", 
                                         font=("Helvetica", 48))
        self.upload_icon_label.pack(pady=(30, 10))
        
        # Upload instructions
        self.upload_instructions = ttk.Label(self.upload_area, 
                                           text="Drag & drop your resume or click below", 
                                           style="TLabel")
        self.upload_instructions.pack(pady=(0, 5))
        
        # Supported formats
        self.format_label = ttk.Label(self.upload_area, 
                                     text="Supported formats: PDF, DOCX, TXT", 
                                     foreground="#95a5a6", 
                                     background=self.background_color)
        self.format_label.pack(pady=(0, 20))
        
        # Browse button
        self.browse_button = ttk.Button(self.upload_area, 
                                      text="Browse Files", 
                                      command=self.browse_file)
        self.browse_button.pack(pady=(0, 30))
        
        # Selected file frame
        self.selected_file_frame = ttk.Frame(self.upload_frame)
        self.selected_file_frame.pack(fill=tk.X, pady=10)
        
        # File info (hidden initially)
        self.file_info_frame = ttk.Frame(self.selected_file_frame)
        self.file_label = ttk.Label(self.file_info_frame, text="", style="TLabel")
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, anchor=tk.W)
        
        # Clear file button (hidden initially)
        self.clear_button = ttk.Button(self.file_info_frame, 
                                     text="✕", 
                                     width=3, 
                                     command=self.clear_file)
        self.clear_button.pack(side=tk.RIGHT)
        
        # Parse button (disabled initially)
        self.parse_button = ttk.Button(self.upload_frame, 
                                     text="Parse Resume", 
                                     command=self.parse_resume, 
                                     state=tk.DISABLED)
        self.parse_button.pack(fill=tk.X, pady=10)
        
        # Export button (hidden initially)
        self.export_button = ttk.Button(self.upload_frame, 
                                      text="Export Results", 
                                      command=self.export_results, 
                                      state=tk.DISABLED)
        self.export_button.pack(fill=tk.X, pady=(0, 10))
        
        # Bind drop events for drag and drop functionality
        self.upload_area.drop_target_register("DND_Files")
        self.upload_area.dnd_bind("<<Drop>>", self.on_drop)
        
    def setup_results_placeholder(self):
        """Set up the placeholder for results section."""
        # Results frame header
        self.results_header = ttk.Label(self.results_frame, 
                                      text="Resume Analysis", 
                                      style="Subheader.TLabel")
        self.results_header.pack(pady=(0, 10), anchor=tk.W)
        
        # Initial placeholder
        self.placeholder_frame = ttk.Frame(self.results_frame, 
                                         style="TFrame", 
                                         borderwidth=2, 
                                         relief=tk.GROOVE)
        self.placeholder_frame.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder message
        self.placeholder_text = ttk.Label(self.placeholder_frame, 
                                        text="Upload and parse a resume to view results", 
                                        style="TLabel",
                                        font=("Helvetica", 12))
        self.placeholder_text.pack(expand=True, pady=100)
        
    def browse_file(self):
        """Open file dialog to browse for resume files."""
        file_types = [
            ("Resume Files", "*.pdf;*.docx;*.txt"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=file_types
        )
        
        if file_path:
            self.set_file(file_path)
    
    def set_file(self, file_path):
        """
        Set the selected file and update UI.
        
        Args:
            file_path (str): Path to the selected file
        """
        self.file_path = file_path
        file_name = os.path.basename(file_path)
        
        # Update file label
        self.file_label.config(text=file_name)
        
        # Show file info frame
        if not self.file_info_frame.winfo_ismapped():
            self.file_info_frame.pack(fill=tk.X, expand=True)
        
        # Enable parse button
        self.parse_button.config(state=tk.NORMAL)
        
        # Update status bar
        self.status_bar.config(text=f"Selected: {file_name}")
    
    def clear_file(self):
        """Clear the selected file."""
        self.file_path = None
        self.file_label.config(text="")
        self.file_info_frame.pack_forget()
        self.parse_button.config(state=tk.DISABLED)
        self.export_button.config(state=tk.DISABLED)
        self.status_bar.config(text="Ready")
        
        # Reset results area
        self.setup_results_placeholder()
    
    def on_drop(self, event):
        """
        Handle drag and drop file event.
        
        Args:
            event: The drop event
        """
        file_path = event.data
        
        # Clean up the file path (depending on the OS)
        if os.name == 'nt':  # Windows
            file_path = file_path.replace('{', '').replace('}', '')
        else:  # Unix/Mac
            file_path = file_path.strip()
        
        # Validate file type
        valid_extensions = ['.pdf', '.docx', '.txt']
        _, ext = os.path.splitext(file_path.lower())
        
        if ext in valid_extensions:
            self.set_file(file_path)
        else:
            messagebox.showerror(
                "Invalid File", 
                f"Please select a PDF, DOCX, or TXT file. Selected: {os.path.basename(file_path)}"
            )
    
    def parse_resume(self):
        """Process the selected resume file."""
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return
        
        # Update status
        self.status_bar.config(text="Parsing resume...")
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            if widget != self.results_header:
                widget.destroy()
        
        # Show processing indicator
        self.processing_frame = ttk.Frame(self.results_frame)
        self.processing_frame.pack(fill=tk.BOTH, expand=True)
        
        self.processing_label = ttk.Label(self.processing_frame, 
                                        text="Processing Resume...", 
                                        style="TLabel",
                                        font=("Helvetica", 14))
        self.processing_label.pack(expand=True, pady=100)
        
        # Update GUI to show processing
        self.root.update()
        
        # Call the processing callback with the file path
        try:
            self.process_callback(self.file_path)
            self.status_bar.config(text="Resume parsed successfully")
        except Exception as e:
            self.status_bar.config(text="Error parsing resume")
            messagebox.showerror("Error", f"Failed to parse resume: {str(e)}")
    
    def enable_export_button(self, callback):
        """
        Enable the export button with the provided callback.
        
        Args:
            callback (function): Function to call when export button is clicked
        """
        self.export_button.config(state=tk.NORMAL, command=callback)
    
    def export_results(self):
        """Placeholder for export results function."""
        # This will be replaced by the actual callback when set
        pass
    
    def get_export_path(self):
        """
        Get the export file path from a save dialog.
        
        Returns:
            str: Selected file path or None if canceled
        """
        file_types = [
            ("JSON Files", "*.json"),
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            title="Save Results",
            filetypes=file_types,
            defaultextension=".json"
        )
        
        return file_path if file_path else None

# Add this to make GUI support drag and drop on Windows
# This is a workaround since tkinterdnd2 isn't included in the code
# In a real implementation, you would import tkinterdnd2
class TkinterDnD:
    """Tkinter drag and drop support simulation."""
    
    @staticmethod
    def drop_target_register(widget, *dndtypes):
        """Register widget as drop target."""
        pass
    
    @staticmethod
    def dnd_bind(widget, sequence, func, add=''):
        """Bind dnd event."""
        pass

# Monkeypatch Frame to have required methods
tk.Frame.drop_target_register = lambda self, *args: None
tk.Frame.dnd_bind = lambda self, *args, **kwargs: None
ttk.Frame.drop_target_register = lambda self, *args: None
ttk.Frame.dnd_bind = lambda self, *args, **kwargs: None