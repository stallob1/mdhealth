#!/usr/bin/env python3
"""
Text File Formatter for Printing
Formats text files to look like printed documents with proper margins, page breaks, and formatting
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import textwrap

class PrintFormatter:
    def __init__(self, 
                 page_width=80,           # Characters per line (standard printer width)
                 margin_left=4,           # Left margin in characters
                 margin_right=4,          # Right margin in characters
                 lines_per_page=60,       # Lines per page (standard 8.5x11 with margins)
                 header=True,            # Include header
                 footer=True,             # Include footer
                 page_numbers=True):      # Include page numbers
        self.page_width = page_width
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.lines_per_page = lines_per_page
        self.header = header
        self.footer = footer
        self.page_numbers = page_numbers
        self.content_width = page_width - margin_left - margin_right
    
    def format_text(self, text, filename):
        """Format text for printing"""
        lines = text.split('\n')
        formatted_lines = []
        current_page = 1
        line_count = 0
        
        # Process each line
        for line in lines:
            # Handle page breaks
            if line.strip().startswith('--- Page'):
                if formatted_lines and formatted_lines[-1].strip():
                    formatted_lines.append('')
                formatted_lines.append(self._create_page_break())
                line_count = 0
                current_page += 1
                continue
            
            # Skip empty lines at start of page
            if line_count == 0 and not line.strip():
                continue
            
            # Wrap long lines
            if len(line) > self.content_width:
                wrapped = textwrap.wrap(line, width=self.content_width, 
                                       initial_indent=' ' * self.margin_left,
                                       subsequent_indent=' ' * self.margin_left)
                for wrapped_line in wrapped:
                    if line_count >= self.lines_per_page:
                        formatted_lines.append(self._create_page_break())
                        line_count = 0
                        current_page += 1
                    formatted_lines.append(wrapped_line)
                    line_count += 1
            else:
                if line_count >= self.lines_per_page:
                    formatted_lines.append(self._create_page_break())
                    line_count = 0
                    current_page += 1
                
                # Add left margin
                if line.strip():
                    formatted_lines.append(' ' * self.margin_left + line)
                else:
                    formatted_lines.append('')
                line_count += 1
        
        # Add final page break if needed
        if formatted_lines and not formatted_lines[-1].startswith('═'):
            formatted_lines.append('')
            formatted_lines.append(self._create_page_break())
        
        # Add headers and footers
        if self.header or self.footer or self.page_numbers:
            formatted_lines = self._add_headers_footers(formatted_lines, filename)
        
        return '\n'.join(formatted_lines)
    
    def _create_page_break(self):
        """Create a visual page break"""
        return '═' * self.page_width
    
    def _add_headers_footers(self, lines, filename):
        """Add headers and footers to formatted text"""
        formatted = []
        current_page = 1
        page_start = 0
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Detect page breaks
            if line.startswith('═'):
                # Add footer to previous page
                if current_page > 1 and self.footer:
                    formatted.insert(page_start, self._create_header(filename, current_page))
                    # Add footer before page break
                    footer_line = len([l for l in formatted[page_start:] if l.strip()])
                    formatted.insert(page_start + footer_line, self._create_footer(current_page))
                
                formatted.append(line)
                current_page += 1
                page_start = len(formatted)
                i += 1
                continue
            
            formatted.append(line)
            i += 1
        
        # Add header/footer to last page
        if self.header:
            formatted.insert(page_start, self._create_header(filename, current_page))
        if self.footer:
            formatted.append(self._create_footer(current_page))
        
        return formatted
    
    def _create_header(self, filename, page_num):
        """Create a header line"""
        header_text = filename[:self.content_width - 20]
        page_text = f"Page {page_num}" if self.page_numbers else ""
        header = f"{header_text:<{self.content_width - len(page_text)}}{page_text}"
        return ' ' * self.margin_left + header
    
    def _create_footer(self, page_num):
        """Create a footer line"""
        date = datetime.now().strftime("%Y-%m-%d")
        footer_text = f"Printed: {date}"
        if self.page_numbers:
            footer_text += f" | Page {page_num}"
        footer = footer_text.center(self.content_width)
        return ' ' * self.margin_left + footer

def format_file(input_path, output_path, formatter):
    """Format a single file"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract filename for header
        filename = Path(input_path).stem
        
        # Format the content
        formatted = formatter.format_text(content, filename)
        
        # Write formatted content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        return True
    except Exception as e:
        print(f"Error formatting {input_path.name}: {e}", file=sys.stderr)
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 format_for_print.py <input_file> [output_file]")
        print("   or: python3 format_for_print.py --all [output_folder]")
        print("\nOptions:")
        print("  --all              Format all .txt files in current directory")
        print("  --output <folder>  Output folder (default: printed_format/)")
        sys.exit(1)
    
    # Create formatter
    formatter = PrintFormatter(
        page_width=80,
        margin_left=4,
        margin_right=4,
        lines_per_page=60,
        header=True,
        footer=True,
        page_numbers=True
    )
    
    if sys.argv[1] == '--all':
        # Format all text files
        output_folder = sys.argv[2] if len(sys.argv) > 2 else 'printed_format'
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)
        
        txt_files = list(Path('.').glob('*.txt'))
        # Exclude already formatted files
        txt_files = [f for f in txt_files if 'printed_format' not in str(f)]
        
        if not txt_files:
            print("No text files found in current directory")
            return
        
        print(f"Found {len(txt_files)} text file(s). Formatting for print...\n")
        success_count = 0
        
        for txt_file in txt_files:
            output_file = output_path / f"{txt_file.stem}_formatted.txt"
            if format_file(txt_file, output_file, formatter):
                print(f"✓ Formatted: {txt_file.name} -> {output_file.name}")
                success_count += 1
        
        print(f"\n✓ Successfully formatted {success_count}/{len(txt_files)} file(s)")
        print(f"  Output folder: {output_path.absolute()}")
    else:
        # Format single file
        input_path = Path(sys.argv[1])
        if len(sys.argv) > 2:
            output_path = Path(sys.argv[2])
        else:
            output_folder = Path('printed_format')
            output_folder.mkdir(exist_ok=True)
            output_path = output_folder / f"{input_path.stem}_formatted.txt"
        
        if format_file(input_path, output_path, formatter):
            print(f"✓ Formatted: {input_path.name} -> {output_path.name}")
        else:
            sys.exit(1)

if __name__ == '__main__':
    main()
