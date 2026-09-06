# AI Resume Evaluator

A Flask web application that uses AI to evaluate resumes. Users can upload a PDF or DOCX resume and receive structured feedback covering resume quality, skills, strengths, weaknesses, structure, ATS readability, missing sections, and actionable recommendations.

## Features

* Accepts PDF and DOCX resume files.
* Extracts text using `pypdf` and `python-docx`.
* Rejects empty documents and documents that do not appear to be resumes/CVs.
* Evaluates resumes using Groq through LangChain.
* Generates an overall resume score out of 100.
* Provides category-based scoring for resume quality.
* Uses anti-hallucination instructions so analysis is based on information present in the uploaded resume.
* Displays the AI response in the browser with Markdown formatting.
* Limits uploads to 10 MB.
* Securely handles uploaded filenames.
* Removes uploaded files when processing fails.

## Requirements

* Python 3.10 or later recommended.
* A Groq API key.
* Windows, macOS, or Linux.

Install the project dependencies with:

```bash
pip install -r requirements.txt
```

## Installation

### 1. Clone or download the project

Open a terminal in the project directory.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do not commit `.env` or expose the API key in source control.

## Run the Application

Start the Flask development server from the project root:

```bash
python app.py
```

Open the application in a browser:

`http://127.0.0.1:5000`

### Upload workflow

1. Select a `.pdf` or `.docx` file no larger than 10 MB.
2. Submit the file through the upload form.
3. The server extracts the document text.
4. The application checks whether the document appears to be a resume/CV.
5. Invalid documents such as certificates, transcripts, assignments, and invoices are rejected.
6. Valid resumes are sent to the Groq model for evaluation.
7. The structured analysis is displayed on the results page.

## AI Evaluation

The application uses the `openai/gpt-oss-120b` model through LangChain's `ChatGroq` integration.

The resume score is divided into five categories:

| Category                          | Maximum Score |
| --------------------------------- | ------------: |
| Content Quality                   |            25 |
| Skills & Experience Presentation  |            20 |
| Structure & Organization          |            20 |
| ATS & Readability                 |            20 |
| Overall Professional Presentation |            15 |
| **Total**                         |       **100** |

The AI is instructed to:

* Identify only skills and facts explicitly present in the resume.
* Avoid inventing candidate information.
* Report missing information as not provided when appropriate.
* Base recommendations on actual weaknesses in the resume.
* Clearly distinguish recommendations from existing candidate information.

## Project Structure

```text
AI Resume Evaluator/
|
|-- app.py
|   Flask routes, file uploads, validation, and request handling
|
|-- analyzer.py
|   Resume validation and AI analysis prompts
|
|-- requirements.txt
|   Python dependencies
|
|-- services/
|   `-- parser.py
|       PDF and DOCX text extraction
|
|-- templates/
|   `-- index.html
|       Upload form and analysis results page
|
|-- static/
|   `-- style.css
|       Application styles
|
|-- uploads/
|   Temporary uploaded files
|
|-- test_analyzer.py
|   Analyzer smoke test
|
|-- test_gemini.py
|   Optional Gemini API diagnostic
|
|-- test_groq.py
|   Groq API smoke test
|
`-- list_groq_models.py
    Lists models available to the configured Groq API key
```

## Testing and Diagnostics

The following scripts make live API calls, so configure the required environment variables before running them.

### Test Groq connection

```bash
python test_groq.py
```

### Run a sample resume analysis

```bash
python test_analyzer.py
```

### List available Groq models

```bash
python list_groq_models.py
```

### Optional Gemini diagnostic

`test_gemini.py` is an optional diagnostic script for Gemini. It requires a separate `GEMINI_API_KEY` and is not used by the Flask application.

```bash
python test_gemini.py
```

## Troubleshooting

### `GROQ_API_KEY was not found`

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Restart the application or command after configuring the key.

### `No module named langchain_groq` or `groq`

Make sure the virtual environment is activated and install the project dependencies:

```bash
pip install -r requirements.txt
```

### No text extracted

The PDF may be image-only or scanned. The current application does not include OCR support. Use a text-based PDF or add OCR functionality before processing scanned documents.

### Document rejected as invalid

The application intentionally rejects documents that do not appear to be resumes/CVs. Examples include certificates, transcripts, assignments, invoices, receipts, and standalone cover letters.

### Upload too large

The application accepts files up to 10 MB.

## Security and Privacy

* Uploaded files are stored temporarily in the `uploads/` directory while they are processed.
* Uploaded filenames are sanitized before being saved.
* Processing errors remove the associated uploaded file.
* Successful uploads are not currently deleted automatically and may remain in the `uploads/` directory.
* Do not use Flask's development server or `debug=True` for production deployment.
* Use HTTPS and appropriate secrets management for deployment.
* Keep API keys in environment variables rather than source code.
* Resume content is sent to the configured AI provider for analysis. Do not upload confidential information unless this is permitted by the applicable privacy requirements.

## Limitations

* The application extracts text only and does not currently perform OCR on scanned documents.
* Formatting evaluation is limited by the text extracted from the uploaded file.
* Analysis quality depends on the extracted text, selected AI model, and Groq API availability.
* The application does not currently include authentication.
* Results are not stored persistently.
* A production WSGI configuration is not included.
