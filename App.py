import streamlit as st
from PIL import Image
import pytesseract
import fitz  
from dotenv import load_dotenv
import google.generativeai as genai
import os

# --- Setup Gemini ---

# Load variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 
model = genai.GenerativeModel("models/gemini-1.5-flash")  

# --- UI ---
st.set_page_config(page_title="Smart Document Parser", layout="centered")
st.title("Smart Document Parser (Gemini)")
st.write("Upload a document (PDF or image) to extract JSON fields.")

uploaded_file = st.file_uploader("Upload a file (PDF, JPG, PNG)", type=["pdf", "jpg", "jpeg", "png"])

# --- Helpers ---
def extract_text_from_pdf(pdf_file):
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
        page = pdf.load_page(0)
        text = page.get_text()
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return text, img

def extract_text_from_image(img_file):
    img = Image.open(img_file)
    text = pytesseract.image_to_string(img)
    return text, img

def build_prompt(doc_text):
    return f"""
Extract the following fields and return only a valid JSON object:

- Name 
- Phone number 
- Email
- LinkedIn
- Github
- Address 
- Education
- Projects
- Experience
- Skills
- Tools
- Achievements
- Certifications
- Activities
- Interests

Instructions: 
- Fields may appear under various labels or headings, or without labels at all
- Make sure to add all the feilds in the JSON
- For missing fields, set their value to null
- For years, separate out the the years into start and end year 
- If only one year mentioned, consider it a start year
- For dates, separate out the the date into start and end date
- If only one date mentioned, consider it a start date
- If both year and date are mentioned, Go with the date
- Output should be raw JSON only — no explanation, no markdown, no extra formatting
- If tools are mentioned within the skills, do not include them under the skill section. Only include them under the Tools section

Here is the document text:
\"\"\"{doc_text}\"\"\"
Return the JSON format below.
"""

def call_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# --- Run ---
if st.button("Enter"):
    if not uploaded_file:
        st.warning("Please upload a file.")
    else:
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            text, preview_img = extract_text_from_pdf(uploaded_file)
            st.image(preview_img, caption="First Page Preview", use_column_width=True)
        else:
            text, preview_img = extract_text_from_image(uploaded_file)
            st.image(preview_img, caption="Uploaded Image", use_column_width=True)

        st.subheader("Extracted Text")
        st.text(text[:1000] + "..." if len(text) > 1000 else text)

        prompt = build_prompt(text)
        st.subheader("Prompt Sent to Gemini")
        st.code(prompt)

        try:
            result = call_gemini(prompt)
            st.subheader("✅ Structured JSON Output")
            st.code(result, language="json")
        except Exception as e:
            st.error(f"Gemini API Error: {e}")
