import os
import re
import sys
import shutil
from datetime import datetime

# Define directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "sources", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "sources", "processed")
NOTES_DIR = os.path.join(BASE_DIR, "notes")

def sanitize_filename(name):
    # Convert to lowercase
    name = name.lower()
    # Replace spaces and dashes with underscores
    name = re.sub(r'[\s\-]+', '_', name)
    name = re.sub(r'[^a-z0-9_.]', '', name)
    return name

def sanitize_title(name):
    # Convert file name into a clean title
    name = os.path.splitext(name)[0]
    name = re.sub(r'[\-_]', ' ', name)
    return name.title()

def get_note_type(filename):
    # Simple heuristics to guess the note type
    lower = filename.lower()
    if 'syllabus' in lower:
        return 'syllabus', ''
    elif any(x in lower for x in ['module', 'unit', 'week', 'lecture', 'recording', 'intro', 'transcript']):
        return 'module', 'modules'
    elif any(x in lower for x in ['reading', 'chapter', 'book', 'article']):
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
            # Deduplicate lines if necessary (e.g. repeated cues)
            if not text_lines or text_lines[-1] != line:
                text_lines.append(line)
        return '\n'.join(text_lines)
    except Exception as e:
        print(f"Error reading VTT {path}: {e}")
        return None

def process_file(filename):
    raw_path = os.path.join(RAW_DIR, filename)
    if not os.path.isfile(raw_path):
        return
    
    if filename.startswith('.'):
        return
        
    print(f"\nProcessing: {filename}")
    
    ext = os.path.splitext(filename)[1].lower()
    
    # Handle media files directly by archiving them
    if ext in ['.mp4', '.m4a', '.mp3', '.mov', '.wav']:
        print(f"Media file detected. Archiving to sources/processed/...")
        try:
            os.makedirs(PROCESSED_DIR, exist_ok=True)
            shutil.move(raw_path, os.path.join(PROCESSED_DIR, filename))
            print(f"Successfully archived: {filename}")
        except Exception as e:
            print(f"Error moving media file: {e}")
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
    else:
        print(f"Unsupported file format: {ext}")
        return

    # Clean up content (e.g. remove excessive newlines)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    note_type, subfolder = get_note_type(filename)
    title = sanitize_title(filename)
    
    # Setup metadata
    today = datetime.today().strftime('%Y-%m-%d')
    frontmatter = f"""---
title: "{title}"
type: "{note_type}"
source: "{filename}"
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
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        shutil.move(raw_path, os.path.join(PROCESSED_DIR, filename))
        print(f"Moved raw file to sources/processed/")
    except Exception as e:
        print(f"Error writing note or moving raw file: {e}")

def main():
    if not os.path.exists(RAW_DIR):
        print(f"Raw directory does not exist: {RAW_DIR}")
        return
        
    files = os.listdir(RAW_DIR)
    raw_files = [f for f in files if os.path.isfile(os.path.join(RAW_DIR, f)) and not f.startswith('.')]
    
    if not raw_files:
        print("No raw files found in sources/raw/ to process.")
        return
        
    print(f"Found {len(raw_files)} file(s) in sources/raw/.")
    for f in raw_files:
        process_file(f)

if __name__ == '__main__':
    main()
