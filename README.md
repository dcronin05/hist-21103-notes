# HIST 21103 Notes

Course notes, readings, and materials for UALR HIST 21103. Organized for publishing and seamless integration into an Obsidian library.

## Directory Structure

- `notes/`: Organized, lowercase Markdown files containing relative markdown links.
  - `notes/syllabus.md`: Course syllabus.
  - `notes/modules/`: Course module summaries and lectures.
  - `notes/readings/`: Textbook chapter summaries and assigned article outlines.
  - `notes/concepts/`: Notes covering historical terms, figures, events, and vocabulary.
- `assets/`: Attachments, maps, diagrams, and other media referenced in the markdown notes.
- `sources/`:
  - `sources/raw/`: Drop incoming raw downloads (PDF, DOCX, TXT) here.
  - `sources/processed/`: Archived raw files after they are converted.

## Material Processing Workflow

To convert raw course materials into Obsidian-compatible markdown notes:

1. Place your raw documents (PDF, DOCX, TXT) in `sources/raw/`.

2. Run the processing script:

   ```bash
   python3 process_materials.py
   ```

   *(Note: PDF and DOCX processing require **`pypdf`** and **`python-docx`** respectively. Install them using **`pip install pypdf python-docx`**.)*

3. The script will parse the files, attach standard YAML frontmatter (with tags/metadata), sanitize the filenames to lowercase and underscores/dashes, output the markdown note into the matching `notes/` subdirectory, and move the raw file to `sources/processed/` for archival.

