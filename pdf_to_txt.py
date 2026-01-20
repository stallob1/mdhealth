#!/usr/bin/env python3
"""
PDF to Text Converter
Extracts text from PDF files and saves them as .txt files
"""

import os
import sys
from pathlib import Path

def extract_text_pypdf2(pdf_path):
    """Extract text using PyPDF2"""
    try:
        import PyPDF2
        text = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                text.append(f"\n--- Page {page_num + 1} ---\n")
                text.append(page.extract_text())
        return '\n'.join(text)
    except ImportError:
        return None
    except Exception as e:
        print(f"Error with PyPDF2: {e}", file=sys.stderr)
        return None

def extract_text_pdfplumber(pdf_path):
    """Extract text using pdfplumber"""
    try:
        import pdfplumber
        text = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text.append(f"\n--- Page {page_num + 1} ---\n")
                text.append(page.extract_text() or "")
        return '\n'.join(text)
    except ImportError:
        return None
    except Exception as e:
        print(f"Error with pdfplumber: {e}", file=sys.stderr)
        return None

def extract_text_pypdf(pdf_path):
    """Extract text using pypdf (newer version of PyPDF2)"""
    try:
        import pypdf
        text = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                text.append(f"\n--- Page {page_num + 1} ---\n")
                text.append(page.extract_text())
        return '\n'.join(text)
    except ImportError:
        return None
    except Exception as e:
        print(f"Error with pypdf: {e}", file=sys.stderr)
        return None

def convert_pdf_to_txt(pdf_path, output_path=None):
    """Convert PDF to text file"""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        return False
    
    if output_path is None:
        output_path = pdf_path.with_suffix('.txt')
    else:
        output_path = Path(output_path)
    
    # Try different PDF libraries in order of preference
    text = None
    
    # Try pypdf first (newest)
    text = extract_text_pypdf(pdf_path)
    
    # Try pdfplumber (better for complex PDFs)
    if not text:
        text = extract_text_pdfplumber(pdf_path)
    
    # Try PyPDF2 (older but common)
    if not text:
        text = extract_text_pypdf2(pdf_path)
    
    if not text:
        print("Error: No PDF extraction library found.")
        print("Install one with: pip3 install pypdf pdfplumber")
        return False
    
    # Clean up text
    text = text.strip()
    
    if not text:
        print(f"Warning: No text extracted from {pdf_path.name}")
        return False
    
    # Write to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Extracted from: {pdf_path.name}\n")
            f.write("=" * 80 + "\n\n")
            f.write(text)
        print(f"✓ Converted: {pdf_path.name} -> {output_path.name}")
        return True
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 pdf_to_txt.py <pdf_file> [output_file]")
        print("   or: python3 pdf_to_txt.py --all  (convert all PDFs in current directory)")
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        # Convert all PDFs in current directory
        pdf_files = list(Path('.').glob('*.pdf'))
        if not pdf_files:
            print("No PDF files found in current directory")
            return
        
        print(f"Found {len(pdf_files)} PDF file(s). Converting...\n")
        success_count = 0
        for pdf_file in pdf_files:
            if convert_pdf_to_txt(pdf_file):
                success_count += 1
        
        print(f"\n✓ Successfully converted {success_count}/{len(pdf_files)} PDF(s)")
    else:
        # Convert single file
        pdf_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        convert_pdf_to_txt(pdf_path, output_path)

if __name__ == '__main__':
    main()
