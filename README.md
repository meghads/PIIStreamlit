Sure! Here is the content you can copy and paste into your `README.md` file, all in one block:

# PII Detection & Redaction App

This is a Python-based application built with **Streamlit**, **Pytesseract**, **PyPDF2**, and **PyMuPDF** to detect and mask Personally Identifiable Information (PII) in documents like PDFs, images, and text files. The application supports detecting and redacting common types of PII including **Aadhaar**, **PAN**, **Driving License**, and **Voter ID**.

## Features
- **PII Detection**: Detects Aadhaar numbers, PAN numbers, Driving Licenses, and Voter IDs using regular expressions.
- **PII Masking**: Replaces detected PII with 'X' characters to ensure privacy.
- **Redaction in PDFs**: If the uploaded document is a PDF, it allows you to redact detected PII directly in the document.
- **Multi-format Support**: Works with various document formats, including PDF, PNG, JPG, JPEG, and TXT.

## Requirements
- Python 3.x
- Required libraries:
  - **Streamlit**: For building the user interface.
  - **Pytesseract**: For Optical Character Recognition (OCR) in images.
  - **PyPDF2**: For extracting text from PDFs.
  - **PyMuPDF (fitz)**: For redacting PII in PDFs.
  - **Pillow (PIL)**: For image handling.

You can install the necessary libraries with the following:

```bash
pip install streamlit pytesseract PyPDF2 fitz pillow
```

Additionally, **Tesseract OCR** needs to be installed on your system. You can download it from the official site: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).

Once installed, make sure to point to the Tesseract executable in the code (`pytesseract.pytesseract.tesseract_cmd`), which in this example is set to `r'C:\Program Files\Tesseract-OCR\tesseract.exe'`. Modify this path based on where Tesseract is installed on your machine.

## How It Works
1. **File Upload**: Upload a document (PDF, PNG, JPG, JPEG, or TXT) using the file uploader.
2. **PII Detection**: The system will process the file and attempt to detect PII such as Aadhaar, PAN, Driving License, and Voter ID using regular expressions.
3. **Redaction in PDFs**: If the file is a PDF, the system will search for detected PII and redact it (replace with a black box). A new redacted PDF can be downloaded.
4. **Masked PII**: The detected PII in the document is replaced with 'X's and displayed in the output.

## File Types Supported
- **PDF**: Text extraction and redaction.
- **Images (PNG, JPG, JPEG)**: Text extraction using OCR.
- **Text Files (TXT)**: Simple text extraction.

## How to Use
1. Run the app:
   ```bash
   streamlit run app.py
   ```
2. Open the app in your web browser (usually at `http://localhost:8501`).
3. Upload a document using the file uploader.
4. The app will display the detected PII and the masked versions.
5. If the document is a PDF, a download button for the redacted PDF will be provided.

## Example Usage

1. **Upload a document**: Choose a document in PDF, image, or text format.
2. **View Results**:
    - The detected PII will be listed.
    - The masked PII will be displayed in JSON format.
3. **Redact PDFs**: If a PDF is uploaded, you can download a redacted version with PII removed.

## Limitations
- PII detection accuracy depends on the quality of the document and the recognition accuracy of Tesseract for OCR-based files.
- The app currently supports basic PII detection for Aadhaar, PAN, Driving License, and Voter ID. You can extend it with more patterns if needed.

