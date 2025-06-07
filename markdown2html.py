#!/usr/bin/python3
"""
A script that converts Markdown files to HTML format.
Supports headings, lists (ordered and unordered), paragraphs,
bold and emphasis text, and special syntax for MD5 hashing and character removal.
"""

import sys
import os
import hashlib
import re

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def remove_c(text):
    return re.sub(r'c', '', text, flags=re.IGNORECASE)

def process_text_formatting(text):
    # Process MD5 syntax
    text = re.sub(r'\[\[(.*?)\]\]', lambda m: md5_hash(m.group(1)), text)
    # Process remove 'c' syntax
    text = re.sub(r'\(\((.*?)\)\)', lambda m: remove_c(m.group(1)), text)
    # Process bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Process emphasis text
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    return text

def convert_markdown_to_html(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Process the content
    lines = content.split('\n')
    html_lines = []
    in_unordered_list = False
    in_ordered_list = False
    in_paragraph = False
    paragraph_lines = []
    
    for line in lines:
        # Handle headings
        if line.startswith('#'):
            if in_unordered_list:
                html_lines.append("</ul>")
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append("</ol>")
                in_ordered_list = False
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            heading_level = len(line.split(' ')[0])
            if 1 <= heading_level <= 6:
                heading_text = process_text_formatting(line[heading_level:].strip())
                html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            continue
        
        # Handle unordered lists
        if line.startswith('- '):
            if in_ordered_list:
                html_lines.append("</ol>")
                in_ordered_list = False
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if not in_unordered_list:
                html_lines.append("<ul>")
                in_unordered_list = True
            list_item = process_text_formatting(line[2:].strip())
            html_lines.append(f"<li>{list_item}</li>")
            continue
        elif in_unordered_list:
            html_lines.append("</ul>")
            in_unordered_list = False
        
        # Handle ordered lists
        if line.startswith('* '):
            if in_unordered_list:
                html_lines.append("</ul>")
                in_unordered_list = False
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if not in_ordered_list:
                html_lines.append("<ol>")
                in_ordered_list = True
            list_item = process_text_formatting(line[2:].strip())
            html_lines.append(f"<li>{list_item}</li>")
            continue
        elif in_ordered_list:
            html_lines.append("</ol>")
            in_ordered_list = False
        
        # Handle paragraphs
        if line.strip():
            if not in_paragraph:
                html_lines.append("<p>")
                in_paragraph = True
            if paragraph_lines:
                html_lines.append("    <br />")
            processed_line = process_text_formatting(line.strip())
            html_lines.append(f"    {processed_line}")
            paragraph_lines.append(line.strip())
        elif in_paragraph:
            html_lines.append("</p>")
            in_paragraph = False
            paragraph_lines = []
    
    # Close any open elements
    if in_unordered_list:
        html_lines.append("</ul>")
    if in_ordered_list:
        html_lines.append("</ol>")
    if in_paragraph:
        html_lines.append("</p>")
    
    html_content = '\n'.join(html_lines)
    
    with open(output_file, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_markdown_to_html(input_file, output_file)
