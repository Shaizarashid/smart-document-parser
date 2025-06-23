# Smart Document Parser (with Gemini + Streamlit)

This project is a lightweight document parser that extracts structured JSON from PDFs or images using OCR and Gemini's generative AI. It showcases skills in prompt engineering, document ingestion pipelines, and JSON-based output control.

---

## Features

- ✅ Upload PDFs or images (JPG/PNG)
- ✅ Extract text using OCR (`pytesseract`) or native PDF parsing
- ✅ Use Gemini Pro (Google AI) to convert messy document text into structured JSON
- ✅ View output in the UI and copy/use as needed
- ✅ Built using lightweight tools (no GPU needed!)

---

## Setup and Run Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/smart-document-parser.git
cd smart-document-parser

### 2. Install all Dependencies

```bash
pip install -r requirements.txt

### 3. Run the application

```bash
streamlit run app.py

### 4. Prompt Optimization

Try out different prompting techniques to fine the one with the best results.




