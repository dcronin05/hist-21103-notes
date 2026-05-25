import os
import re
import sys
import shutil
import html
from datetime import datetime
from html.parser import HTMLParser

# Define directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "sources", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "sources", "processed")
NOTES_DIR = os.path.join(BASE_DIR, "notes")

class HTMLToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.stack = []
        self.in_header = False
        self.header_level = 0
        self.in_blockquote = False
        self.list_stack = []  # contains 'ul' or 'ol'
        self.in_list_item = False
        self.bold_depth = 0
        self.italic_depth = 0
        self.link_url = None
        self.first_header = None
        self.current_header_text = []
        self.in_title = False
        self.html_title = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.stack.append(tag)
        
        if tag == 'title':
            self.in_title = True
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_header = True
            self.header_level = int(tag[1])
            self.result.append('\n\n' + '#' * self.header_level + ' ')
            self.current_header_text = []
        elif tag == 'p':
            self.result.append('\n\n')
        elif tag == 'br':
            self.result.append('\n')
        elif tag in ['em', 'i']:
            self.italic_depth += 1
            self.result.append('*')
        elif tag in ['strong', 'b']:
            self.bold_depth += 1
            self.result.append('**')
        elif tag == 'blockquote':
            self.in_blockquote = True
            self.result.append('\n\n> ')
        elif tag in ['ul', 'ol']:
            self.list_stack.append(tag)
            self.result.append('\n')
        elif tag == 'li':
            self.in_list_item = True
            indent = '  ' * (len(self.list_stack) - 1)
            if self.list_stack and self.list_stack[-1] == 'ol':
                self.result.append(f'\n{indent}1. ')
            else:
                self.result.append(f'\n{indent}* ')
        elif tag == 'a' and 'href' in attrs_dict:
            self.link_url = attrs_dict['href']
            self.result.append('[')

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
            
        if tag == 'title':
            self.in_title = False
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_header = False
            header_str = ''.join(self.current_header_text).strip()
            if not self.first_header and header_str:
                self.first_header = header_str
            self.result.append('\n\n')
        elif tag == 'p':
            self.result.append('\n\n')
        elif tag in ['em', 'i']:
            self.italic_depth = max(0, self.italic_depth - 1)
            self.result.append('*')
        elif tag in ['strong', 'b']:
            self.bold_depth = max(0, self.bold_depth - 1)
            self.result.append('**')
        elif tag == 'blockquote':
            self.in_blockquote = False
            self.result.append('\n\n')
        elif tag in ['ul', 'ol']:
            if self.list_stack:
                self.list_stack.pop()
            self.result.append('\n')
        elif tag == 'li':
            self.in_list_item = False
        elif tag == 'a' and self.link_url:
            self.result.append(f']({self.link_url})')
            self.link_url = None

    def handle_data(self, data):
        text = html.unescape(data)
        if self.in_title:
            self.html_title = text.strip()
        if self.in_header:
            self.current_header_text.append(text)
            
        if not self.in_header and not self.in_list_item and not self.in_blockquote:
            text = re.sub(r'\s+', ' ', text)
            
        self.result.append(text)

    def get_markdown(self):
        raw = ''.join(self.result)
        raw = re.sub(r'\n{3,}', '\n\n', raw)
        raw = re.sub(r' +', ' ', raw)
        raw = re.sub(r'\*\s+', '*', raw)
        raw = re.sub(r'\s+\*', '*', raw)
        raw = re.sub(r'\*\*\s+', '**', raw)
        raw = re.sub(r'\s+\*\*', '**', raw)
        return raw.strip()

def sanitize_filename(name):
    name = name.lower()
    name = re.sub(r'[\s\-]+', '_', name)
    name = re.sub(r'[^a-z0-9_.]', '', name)
    # Remove double underscores
    name = re.sub(r'_+', '_', name)
    return name.strip('_')

def sanitize_title(name):
    name = os.path.splitext(name)[0]
    name = re.sub(r'[\-_]', ' ', name)
    return name.title()

def get_note_type(filename):
    lower = filename.lower()
    if 'syllabus' in lower:
        return 'syllabus', ''
    elif any(x in lower for x in ['essay', 'assignment', 'prompt', 'instructions']):
        return 'assignment', 'assignments'
    elif any(x in lower for x in ['module', 'unit', 'week', 'lecture', 'recording', 'intro', 'transcript']):
        return 'module', 'modules'
    elif any(x in lower for x in ['reading', 'chapter', 'book', 'article', 'biography', 'scholarly', 'columbus']):
        return 'reading', 'readings'
    else:
        return 'concept', 'concepts'

def extract_pdf_text(path):
    try:
        import pypdf
    except ImportError:
        print("Dependency 'pypdf' is missing. Please run: pip install pypdf")
        return None
    
    try:
        reader = pypdf.PdfReader(path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF {path}: {e}")
        return None

def extract_docx_text(path):
    try:
        import docx
    except ImportError:
        print("Dependency 'python-docx' is missing. Please run: pip install python-docx")
        return None
    
    try:
        doc = docx.Document(path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    except Exception as e:
        print(f"Error reading DOCX {path}: {e}")
        return None

def extract_vtt_text(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        text_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                continue
            if '-->' in line:
                continue
            if line.isdigit():
                continue
            if not text_lines or text_lines[-1] != line:
                text_lines.append(line)
        return '\n'.join(text_lines)
    except Exception as e:
        print(f"Error reading VTT {path}: {e}")
        return None

def extract_html_text(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        parser = HTMLToMarkdown()
        parser.feed(html_content)
        return parser.get_markdown()
    except Exception as e:
        print(f"Error reading HTML {path}: {e}")
        return None

def process_file(rel_path):
    raw_path = os.path.join(RAW_DIR, rel_path)
    if not os.path.isfile(raw_path):
        return
        
    filename = os.path.basename(rel_path)
    if filename.startswith('.'):
        return
        
    print(f"\nProcessing: {rel_path}")
    
    ext = os.path.splitext(filename)[1].lower()
    
    # Handle media files directly by archiving
    if ext in ['.mp4', '.m4a', '.mp3', '.mov', '.wav']:
        print(f"Media file detected. Archiving to sources/processed/...")
        archive_raw_file(rel_path)
        return

    content = ""
    
    if ext == '.txt':
        try:
            with open(raw_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading text file: {e}")
            return
    elif ext == '.vtt':
        content = extract_vtt_text(raw_path)
        if content is None:
            return
    elif ext == '.pdf':
        content = extract_pdf_text(raw_path)
        if content is None:
            return
    elif ext in ['.docx', '.doc']:
        content = extract_docx_text(raw_path)
        if content is None:
            return
    elif ext in ['.html', '.xhtml']:
        content = extract_html_text(raw_path)
        if content is None:
            return
    else:
        print(f"Unsupported file format: {ext}")
        return

    # Clean up content
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    note_type, subfolder = get_note_type(filename)
    title = sanitize_title(filename)
    
    # Setup metadata
    today = datetime.today().strftime('%Y-%m-%d')
    frontmatter = f"""---
title: "{title}"
type: "{note_type}"
source: "{rel_path}"
date_added: {today}
tags:
  - hist_21103
  - {note_type}
---

"""
    # Create final note body
    note_body = frontmatter + f"# {title}\n\n" + content
    
    # Decide output location
    clean_name = sanitize_filename(os.path.splitext(filename)[0] + ".md")
    if subfolder:
        out_dir = os.path.join(NOTES_DIR, subfolder)
    else:
        out_dir = NOTES_DIR
        
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, clean_name)
    
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(note_body)
        print(f"Created note: {os.path.relpath(out_path, BASE_DIR)}")
        
        # Move raw file to processed
        archive_raw_file(rel_path)
        
        # Check for associated _files directory (common for saved HTML pages)
        base_no_ext = os.path.splitext(raw_path)[0]
        files_dir = base_no_ext + "_files"
        if os.path.exists(files_dir) and os.path.isdir(files_dir):
            rel_files_dir = os.path.splitext(rel_path)[0] + "_files"
            archive_raw_dir(rel_files_dir)
            
    except Exception as e:
        print(f"Error writing note or moving raw file: {e}")

def archive_raw_file(rel_path):
    raw_path = os.path.join(RAW_DIR, rel_path)
    dest_path = os.path.join(PROCESSED_DIR, rel_path)
    dest_dir = os.path.dirname(dest_path)
    
    os.makedirs(dest_dir, exist_ok=True)
    if os.path.exists(dest_path):
        os.remove(dest_path)
    shutil.move(raw_path, dest_path)
    print(f"Archived file: sources/raw/{rel_path} -> sources/processed/{rel_path}")

def archive_raw_dir(rel_path):
    raw_path = os.path.join(RAW_DIR, rel_path)
    dest_path = os.path.join(PROCESSED_DIR, rel_path)
    
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    shutil.move(raw_path, dest_path)
    print(f"Archived folder: sources/raw/{rel_path} -> sources/processed/{rel_path}")

def main():
    if not os.path.exists(RAW_DIR):
        print(f"Raw directory does not exist: {RAW_DIR}")
        return
        
    # Traverse RAW_DIR recursively
    raw_files = []
    for root, dirs, files in os.walk(RAW_DIR):
        for file in files:
            if file.startswith('.'):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, RAW_DIR)
            raw_files.append(rel_path)
            
    if not raw_files:
        print("No raw files found in sources/raw/ to process.")
        return
        
    print(f"Found {len(raw_files)} file(s) in sources/raw/.")
    for f in sorted(raw_files):
        process_file(f)

if __name__ == '__main__':
    main()
