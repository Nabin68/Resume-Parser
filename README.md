# Resume Parser - Desktop Application

A Python desktop application built with Tkinter that uses Cohere's AI API to intelligently extract and organize relevant information from candidate resumes.

## Features

- **Upload Support**: Process resumes in PDF, DOCX, and TXT formats
- **Intelligent Parsing**: Uses Cohere's AI API to extract structured information from resumes
- **Clean Interface**: User-friendly desktop application with intuitive controls
- **Export Options**: Save parsed data in JSON or CSV formats
- **Offline Processing**: Runs locally for faster performance (requires internet only for API calls)

## Extracted Information

The application extracts the following information from resumes:

- Full Name
- Contact Details (Email, Phone)
- Skills
- Education History
- Work Experience
- Projects or Certifications

## Installation

### Prerequisites

- Python 3.8 or higher
- Cohere API Key (get one at [cohere.com](https://cohere.com))

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/resume-parser-desktop.git
   cd resume-parser-desktop
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add your Cohere API key:
   ```
   COHERE_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. In the application:
   - Click "Upload Resume" to select a resume file (PDF, DOCX, or TXT)
   - Click "Parse Resume" to extract information
   - View the structured data in the interface
   - Optionally save the results using the "Export" menu

## Project Structure

```
resume_parser_desktop/
│
├── main.py                 # Application entry point
├── gui/
│   └── interface.py        # Tkinter user interface
├── reader/
│   └── file_reader.py      # File reading for different formats
├── preprocessor/
│   └── cleaner.py          # Text preprocessing module
├── parser/
│   └── cohere_parser.py    # Handles Cohere API communication
├── display/
│   └── result_display.py   # Formats and displays parsed results
├── exporter/
│   └── save.py             # Exports results to JSON/CSV
├── utils/
│   └── helper.py           # Shared utility functions
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Dependencies

- **Python**: Core programming language
- **Tkinter**: GUI framework
- **pdfplumber**: PDF text extraction
- **python-docx**: DOCX file reading
- **Cohere API**: AI-based text understanding
- **python-dotenv**: Environment variable management
- **customtkinter**: Enhanced Tkinter widgets for modern UI
- **ttkthemes**: Additional themes for Tkinter

## Tips for Best Results

- For best parsing results, ensure resumes are well-formatted and clearly structured
- The application works best with standard resume layouts
- The AI parser will attempt to identify relevant information even from less structured documents

## License

MIT License

## Acknowledgements

- [Cohere](https://cohere.com) for providing the AI API
- All open source libraries used in this project