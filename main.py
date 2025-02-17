import os
import re
import streamlit as st
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

# Setup upload folder
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Pytesseract setup
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# PII Regex Patterns
aadhaar_pattern = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
pan_pattern = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b')
dl_pattern = re.compile(r'\b[0-9]{2}[A-Z]{2}[0-9]{2,7}\b')
voter_id_pattern = re.compile(r'\b[A-Z]{3}[0-9]{7}\b')

# Function to extract text from files
def extract_text(file_path):
    text = ''
    if file_path.lower().endswith('.pdf'):
        reader = PdfReader(file_path)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        text = pytesseract.image_to_string(Image.open(file_path), config='--psm 6')
    elif file_path.lower().endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    return text

# Function to detect and mask PII
def detect_and_mask_pii(text):
    masked_pii = {
        'aadhaar': [re.sub(r'\S', 'X', match) for match in aadhaar_pattern.findall(text)],
        'pan': [re.sub(r'\S', 'X', match) for match in pan_pattern.findall(text)],
        'driving_license': [re.sub(r'\S', 'X', match) for match in dl_pattern.findall(text)],
        'voter_id': [re.sub(r'\S', 'X', match) for match in voter_id_pattern.findall(text)]
    }
    pii_found = {
        'aadhaar': aadhaar_pattern.findall(text),
        'pan': pan_pattern.findall(text),
        'driving_license': dl_pattern.findall(text),
        'voter_id': voter_id_pattern.findall(text)
    }
    return pii_found, masked_pii

# Function to redact PII in PDF
def redact_pii_in_pdf(pdf_path, pii_data):
    doc = fitz.open(pdf_path)
    redacted = False
    for page in doc:
        for pii_list in pii_data.values():
            for pii in pii_list:
                text_instances = page.search_for(pii)
                if text_instances:
                    redacted = True
                    for inst in text_instances:
                        page.add_redact_annot(inst, fill=(0, 0, 0))
        if redacted:
            page.apply_redactions()
    modified_pdf_path = os.path.join(UPLOAD_FOLDER, 'redacted_' + os.path.basename(pdf_path))
    doc.save(modified_pdf_path, deflate=True)
    doc.close()
    return modified_pdf_path if redacted else None

# Streamlit UI
st.title("PII Detection & Redaction App")
file = st.file_uploader("Upload a document (PDF, PNG, JPG, TXT)", type=["pdf", "png", "jpg", "jpeg", "txt"])

if file:
    file_path = os.path.join(UPLOAD_FOLDER, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    
    st.success("File uploaded successfully!")
    text = extract_text(file_path)
    pii_results, masked_pii = detect_and_mask_pii(text)
    
    if any(pii_results.values()):
        st.subheader("Detected PII")
        st.json(pii_results)
        
        st.subheader("Masked PII")
        st.json(masked_pii)
        
        if file.name.endswith('.pdf'):
            modified_pdf_path = redact_pii_in_pdf(file_path, pii_results)
            if modified_pdf_path:
                with open(modified_pdf_path, "rb") as f:
                    st.download_button("Download Redacted PDF", f, file_name="redacted_pii.pdf")
            else:
                st.warning("No PII found for redaction in the PDF.")
    else:
        st.warning("No PII detected in the document.")
