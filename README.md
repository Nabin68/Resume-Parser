# Resume Parser

A tool that automates the extraction and organization of key information from resumes using the Cohere API. This application processes resumes in various formats (PDF, DOCX, TXT) and extracts structured information like contact details, skills, education, and work experience.

## Features

- Upload resumes in PDF, DOCX, or TXT formats
- Extract key information using Cohere's AI
- View extracted data in a clean, organized format
- Export parsed data as JSON or CSV

## Setup and Installation

1. Clone this repository:
```
git clone <repository-url>
cd resume-parser-project
```

2. Install required dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file in the project root directory and add your Cohere API key:
```
COHERE_API_KEY=your_api_key_here
```

4. Run the application:
```
streamlit run main.py
```

## Project Structure

```
resume_parser_project/
│
├── main.py                       # Entry point – connects all modules
├── gui/                          # GUI components
│   └── interface.py
├── reader/                       # File reading logic
│   └── file_reader.py
├── preprocessor/
│   └── cleaner.py                # Text cleaning functions
├── parser/
│   └── cohere_parser.py          # Cohere API calls & parsing
├── display/
│   └── result_display.py         # Show parsed fields in UI
├── exporter/                     # Export to CSV/JSON
│   └── save.py
├── utils/
│   └── helper.py                 # Any shared utility functions
├── requirements.txt              # List of dependencies
└── README.md
```

## Usage

1. Launch the application
2. Upload a resume file (PDF, DOCX, or TXT)
3. Click "Parse Resume"
4. View the extracted information
5. Export the data if needed (JSON or CSV)

## Dependencies

- Streamlit: For the web interface
- pdfplumber: For reading PDF files
- python-docx: For reading DOCX files
- python-dotenv: For loading environment variables
- cohere: For accessing the Cohere API
- pandas: For data manipulation and export