import os
import re
import shutil
import zipfile
import html
from datetime import datetime
from html.parser import HTMLParser

# Define directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "sources", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "sources", "processed")
OUT_DIR = os.path.join(BASE_DIR, "notes", "readings", "1619")

EPUB_NAME = "Horn, James - 1619- Jamestown and the Forging of American Democracy.epub"

# Locate EPUB in either raw or processed directory
if os.path.exists(os.path.join(RAW_DIR, EPUB_NAME)):
    EPUB_PATH = os.path.join(RAW_DIR, EPUB_NAME)
else:
    EPUB_PATH = os.path.join(PROCESSED_DIR, EPUB_NAME)

class EPUBHTMLToMarkdown(HTMLParser):
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

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.stack.append(tag)
        
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
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
            if not self.in_header:
                url = attrs_dict['href']
                # Rewrite references for pseudo-wiki links between parsed chapters
                url = re.sub(r'chapter001\.xhtml', 'chapter_01.md', url)
                url = re.sub(r'chapter002\.xhtml|chapter003\.xhtml|chapter004\.xhtml', 'chapter_02.md', url)
                url = re.sub(r'chapter005\.xhtml', 'chapter_03.md', url)
                url = re.sub(r'chapter006\.xhtml', 'chapter_04.md', url)
                url = re.sub(r'chapter007\.xhtml|chapter008\.xhtml|chapter009\.xhtml', 'chapter_05.md', url)
                url = re.sub(r'chapter010\.xhtml', 'chapter_06.md', url)
                url = re.sub(r'chapter011\.xhtml', 'epilogue.md', url)
                url = re.sub(r'introduction\.xhtml', 'introduction.md', url)
                url = re.sub(r'preface001\.xhtml', 'preface.md', url)
                url = re.sub(r'preface003\.xhtml', 'authors_note.md', url)
                url = re.sub(r'acknowledgements\.xhtml', 'acknowledgements.md', url)
                url = re.sub(r'personblurb\.xhtml', 'about_the_author.md', url)
                url = re.sub(r'endnotes\.xhtml', 'endnotes.md', url)
                url = re.sub(r'appendix001\.xhtml', 'book_index.md', url)
                self.link_url = url
                self.result.append('[')

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
            
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
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
        elif tag == 'a':
            if not self.in_header and self.link_url:
                self.result.append(f']({self.link_url})')
                self.link_url = None

    def handle_data(self, data):
        text = html.unescape(data)
        if self.in_header:
            self.current_header_text.append(text)
            
        if not self.in_header and not self.in_list_item and not self.in_blockquote:
            text = re.sub(r'\s+', ' ', text)
            
        self.result.append(text)

    def get_markdown(self):
        raw = ''.join(self.result)
        raw = re.sub(r'\r\n', '\n', raw)
        # Convert lines containing only spaces/tabs to empty lines
        raw = re.sub(r'\n[ \t]+\n', '\n\n', raw)
        raw = re.sub(r'\n{3,}', '\n\n', raw)
        raw = re.sub(r' +', ' ', raw)
        raw = re.sub(r'\*[ \t]+', '*', raw)
        raw = re.sub(r'[ \t]+\*', '*', raw)
        raw = re.sub(r'\*\*[ \t]+', '**', raw)
        raw = re.sub(r'[ \t]+\*\*', '**', raw)
        return raw.strip()

# Define the merged grouping plan based on table of contents
GROUPS = [
    {
        "out": "copyright.md",
        "title": "Copyright & Licensing",
        "chapter_num": None,
        "files": ["OEBPS/copyright.xhtml"]
    },
    {
        "out": "dedication.md",
        "title": "Dedication & Epigraph",
        "chapter_num": None,
        "files": ["OEBPS/dedication.xhtml", "OEBPS/epigraph.xhtml"]
    },
    {
        "out": "preface.md",
        "title": "Preface",
        "chapter_num": None,
        "files": ["OEBPS/preface001.xhtml"]
    },
    {
        "out": "authors_note.md",
        "title": "Author's Note",
        "chapter_num": None,
        "files": ["OEBPS/preface003.xhtml"]
    },
    {
        "out": "introduction.md",
        "title": "Introduction: 1619",
        "chapter_num": 0,
        "files": ["OEBPS/introduction.xhtml"]
    },
    {
        "out": "chapter_01.md",
        "title": "Chapter One: Jamestown",
        "chapter_num": 1,
        "files": ["OEBPS/chapter001.xhtml"]
    },
    {
        "out": "chapter_02.md",
        "title": "Chapter Two: The Great Reforms",
        "chapter_num": 2,
        "files": ["OEBPS/chapter002.xhtml", "OEBPS/chapter003.xhtml", "OEBPS/chapter004.xhtml"]
    },
    {
        "out": "chapter_03.md",
        "title": "Chapter Three: First Africans",
        "chapter_num": 3,
        "files": ["OEBPS/chapter005.xhtml"]
    },
    {
        "out": "chapter_04.md",
        "title": "Chapter Four: Commonwealth",
        "chapter_num": 4,
        "files": ["OEBPS/chapter006.xhtml"]
    },
    {
        "out": "chapter_05.md",
        "title": "Chapter Five: Tumult and Liberty",
        "chapter_num": 5,
        "files": ["OEBPS/chapter007.xhtml", "OEBPS/chapter008.xhtml", "OEBPS/chapter009.xhtml"]
    },
    {
        "out": "chapter_06.md",
        "title": "Chapter Six: Inequality and Freedom",
        "chapter_num": 6,
        "files": ["OEBPS/chapter010.xhtml"]
    },
    {
        "out": "epilogue.md",
        "title": "Epilogue: After 1619",
        "chapter_num": 7,
        "files": ["OEBPS/chapter011.xhtml"]
    },
    {
        "out": "acknowledgements.md",
        "title": "Acknowledgments",
        "chapter_num": None,
        "files": ["OEBPS/acknowledgements.xhtml"]
    },
    {
        "out": "about_the_author.md",
        "title": "About the Author",
        "chapter_num": None,
        "files": ["OEBPS/personblurb.xhtml"]
    },
    {
        "out": "endnotes.md",
        "title": "Notes & References",
        "chapter_num": None,
        "files": ["OEBPS/endnotes.xhtml"]
    },
    {
        "out": "book_index.md",
        "title": "Book Index",
        "chapter_num": None,
        "files": ["OEBPS/appendix001.xhtml"]
    }
]

def main():
    if not os.path.exists(EPUB_PATH):
        print(f"EPUB file not found: {EPUB_PATH}")
        return

    print(f"Opening EPUB: {EPUB_PATH}")
    
    # Delete old output directory if it exists to clean up old fragmented files
    if os.path.exists(OUT_DIR):
        print("Cleaning up old parsed files...")
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR, exist_ok=True)

    today = datetime.today().strftime('%Y-%m-%d')

    with zipfile.ZipFile(EPUB_PATH, 'r') as z:
        for g in GROUPS:
            combined_md = []
            
            for file_path in g["files"]:
                try:
                    html_content = z.read(file_path).decode('utf-8', errors='ignore')
                except KeyError:
                    # In case paths are structured differently in the zip
                    short_path = os.path.basename(file_path)
                    try:
                        html_content = z.read(short_path).decode('utf-8', errors='ignore')
                    except KeyError:
                        print(f"Could not find file {file_path} inside EPUB.")
                        continue
                
                parser = EPUBHTMLToMarkdown()
                parser.feed(html_content)
                md = parser.get_markdown()
                if md:
                    combined_md.append(md)
            
            # Combine content from merged files
            full_body = "\n\n***\n\n".join(combined_md)
            
            # Skip empty nodes
            if not full_body.strip():
                continue
                
            # Construct frontmatter
            frontmatter = f"""---
title: "{g['title']}"
type: "reading"
book: "1619: Jamestown and the Forging of American Democracy"
author: "James Horn"
"""
            if g["chapter_num"] is not None:
                frontmatter += f"chapter_num: {g['chapter_num']}\n"
                
            frontmatter += f"""source: "{EPUB_NAME}"
date_added: {today}
tags:
  - hist_21103
  - reading
  - 1619
---

"""
            full_note = frontmatter + full_body
            out_file = os.path.join(OUT_DIR, g["out"])
            
            with open(out_file, 'w', encoding='utf-8') as f_out:
                f_out.write(full_note)
            print(f"Created merged note: notes/readings/1619/{g['out']} -> {g['title']}")

    # Ensure raw EPUB is in processed folder
    if EPUB_PATH.startswith(RAW_DIR):
        try:
            os.makedirs(PROCESSED_DIR, exist_ok=True)
            shutil.move(EPUB_PATH, os.path.join(PROCESSED_DIR, EPUB_NAME))
            print("Moved raw EPUB to sources/processed/")
        except Exception as e:
            print(f"Error archiving EPUB: {e}")

    print("\nEPUB merging and processing complete!")

if __name__ == '__main__':
    main()
