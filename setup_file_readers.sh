#!/bin/bash

# Setup script for file reading capabilities
# Installs all necessary tools and libraries

echo "Setting up file reading tools..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required"
    exit 1
fi

echo "✓ Python 3 found"

# Install Python libraries
echo ""
echo "Installing Python libraries..."
pip3 install --user pdfplumber python-pptx python-docx openpyxl Pillow pytesseract SpeechRecognition pydub 2>&1 | grep -E "(Successfully|Requirement|Error)" | tail -5

# Check for Tesseract OCR (required for image OCR)
if ! command -v tesseract &> /dev/null; then
    echo ""
    echo "⚠ Tesseract OCR not found. To enable image OCR:"
    echo "   brew install tesseract"
    echo ""
else
    echo "✓ Tesseract OCR found"
fi

# Check for ffmpeg (helpful for audio processing)
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "ℹ ffmpeg not found (optional, for better audio processing):"
    echo "   brew install ffmpeg"
    echo ""
else
    echo "✓ ffmpeg found"
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "Available tools:"
echo "  - pdf_to_txt.py          : Extract text from PDFs"
echo "  - extract_all_files.py   : Extract text from PDFs, PPTX, DOCX, XLSX, audio, images"
echo "  - format_for_print.py    : Format text files for printing"
echo ""
echo "Usage examples:"
echo "  python3 extract_all_files.py --all"
echo "  python3 extract_all_files.py file.pptx output.txt"
