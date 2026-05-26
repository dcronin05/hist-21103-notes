#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import datetime
import sys
import os

# Raw dataset matching the course plan
tasks_data = [
    {
        "name": "Syllabus Review & Course Orientation",
        "description": "Read the course syllabus, review communication and grading policies, and outline the calendar in ClickUp.\n\n### Checklist:\n- [ ] Read the full course syllabus.\n- [ ] Read the course introduction lecture transcript.\n- [ ] Mark the June 29 final course deadline.",
        "start_date": "05/25/2026",
        "due_date": "05/27/2026",
        "priority": 3,  # Normal
        "points": 0,
        "subtasks": [
            "Read course syllabus notes/syllabus.md",
            "Review welcome lecture notes/modules/course_introduction_transcript.md",
            "Set up ClickUp tasks and milestone tracking"
        ]
    },
    {
        "name": "Essay One: Columbus Analysis",
        "description": "Contrast the traditional biography of Christopher Columbus with Abbas Hamdani's thesis on apocalyptic crusader motivations.\n\n### Requirements:\n- Length: 2-3 pages, double-spaced.\n- Font: Times New Roman, 12pt.\n- Value: 50 points.\n\n### Checklist:\n- [ ] Read Christopher Columbus Biography (Traditional Narrative).\n- [ ] Read 'Columbus and the Recovery of Jerusalem' by Abbas Hamdani.\n- [ ] Study the professor's video lecture transcript.\n- [ ] Write comparative narrative.\n- [ ] Submit on Blackboard.",
        "start_date": "05/26/2026",
        "due_date": "05/31/2026",
        "priority": 2,  # High
        "points": 50,
        "subtasks": [
            "Read reading notes/readings/christopher_columbus_biography.md",
            "Read article notes/readings/columbus_and_the_recovery_of_jerusalem.md",
            "Review Columbus lecture notes/assignments/columbus_essay_video_notes.md",
            "Draft comparative analysis",
            "Submit Essay One on Blackboard portal"
        ]
    },
    {
        "name": "Book Essay 1: Colonial Settlement (Horn Intro & Ch 1)",
        "description": "Write a book response analyzing James Horn's Introduction & Chapter 1 on Jamestown.\n\n### Requirements:\n- Length: 1-2 pages.\n- Value: 25 points.\n\n### Checklist:\n- [ ] Read Introduction to 1619.\n- [ ] Read Chapter 1 (Jamestown).\n- [ ] Study Dr. Ross's Colonial Settlement Video Notes.\n- [ ] Write response essay.\n- [ ] Submit on Blackboard.",
        "start_date": "05/28/2026",
        "due_date": "06/02/2026",
        "priority": 3,  # Normal
        "points": 25,
        "subtasks": [
            "Read reading notes/readings/1619/introduction.md",
            "Read reading notes/readings/1619/chapter_01.md",
            "Review video notes/assignments/colonial_settlement_video_notes.md",
            "Draft Jamestown response essay",
            "Submit Book Essay 1 on Blackboard"
        ]
    },
    {
        "name": "Book Essay 2: The Great Reforms (Horn Ch 2)",
        "description": "Write a short response analyzing Sir Edwin Sandys's 1619 reforms regarding liberty, property, and governance.\n\n### Requirements:\n- Length: 1-2 pages.\n- Value: 25 points.\n\n### Checklist:\n- [ ] Read Horn Chapter 2 (The Great Reforms).\n- [ ] Study Great Reforms Video Notes.\n- [ ] Draft response essay.\n- [ ] Submit on Blackboard.",
        "start_date": "06/01/2026",
        "due_date": "06/06/2026",
        "priority": 3,  # Normal
        "points": 25,
        "subtasks": [
            "Read reading notes/readings/1619/chapter_02.md",
            "Review video notes/assignments/great_reforms_video_notes.md",
            "Draft Edwin Sandys reform response",
            "Submit Book Essay 2 on Blackboard"
        ]
    },
    {
        "name": "Book Essay 3: First Africans (Horn Ch 3)",
        "description": "Write a response to Horn's Chapter 3 regarding the arrival of first Africans and early labor conditions.\n\n### Requirements:\n- Length: 1-2 pages.\n- Value: 25 points.\n\n### Checklist:\n- [ ] Read Horn Chapter 3 (First Africans).\n- [ ] Study First Africans Video Notes.\n- [ ] Draft response essay.\n- [ ] Submit on Blackboard.",
        "start_date": "06/03/2026",
        "due_date": "06/09/2026",
        "priority": 3,  # Normal
        "points": 25,
        "subtasks": [
            "Read reading notes/readings/1619/chapter_03.md",
            "Review video notes/assignments/first_africans_video_notes.md",
            "Draft First Africans response",
            "Submit Book Essay 3 on Blackboard"
        ]
    },
    {
        "name": "Book Essay 4: Commonwealth (Horn Ch 4)",
        "description": "Write a short response to Horn's Chapter 4 regarding the Christian Commonwealth model in early VA.\n\n### Requirements:\n- Length: 1-2 pages.\n- Value: 25 points.\n\n### Checklist:\n- [ ] Read Horn Chapter 4 (Commonwealth).\n- [ ] Study Commonwealth Video Notes.\n- [ ] Draft response essay.\n- [ ] Submit on Blackboard.",
        "start_date": "06/08/2026",
        "due_date": "06/12/2026",
        "priority": 3,  # Normal
        "points": 25,
        "subtasks": [
            "Read reading notes/readings/1619/chapter_04.md",
            "Review video notes/assignments/commonwealth_video_notes.md",
            "Draft Christian Commonwealth response",
            "Submit Book Essay 4 on Blackboard"
        ]
    },
    {
        "name": "Book Essay 5: Tumult and Liberty (Horn Ch 5)",
        "description": "Write a response to Horn's Chapter 5 regarding the 1622 massacre and the shift in Native relations.\n\n### Requirements:\n- Length: 1-2 pages.\n- Value: 25 points.\n\n### Checklist:\n- [ ] Read Horn Chapter 5 (Tumult and Liberty).\n- [ ] Study Tumult & Liberty Video Notes.\n- [ ] Draft response essay.\n- [ ] Submit on Blackboard.",
        "start_date": "06/10/2026",
        "due_date": "06/14/2026",
        "priority": 3,  # Normal
        "points": 25,
        "subtasks": [
            "Read reading notes/readings/1619/chapter_05.md",
            "Review video notes/assignments/tumult_and_liberty_video_notes.md",
            "Draft 1622 Massacre response",
            "Submit Book Essay 5 on Blackboard"
        ]
    },
    {
        "name": "Major Essay Two: Voices of the American Revolution",
        "description": "Write a comparative/contrast narrative using exactly 10 primary source documents (2 from each group A through E).\n\n### Requirements:\n- Length: 3-5 pages.\n- Font: 12-point font, double-spaced.\n- Value: 50 points.\n\n### Checklist:\n- [ ] Read 2 documents from Group A (Religious).\n- [ ] Read 2 documents from Group B (Loyalist).\n- [ ] Read 2 documents from Group C (Rebel).\n- [ ] Read 2 documents from Group D (African American).\n- [ ] Read 2 documents from Group E (Official/Legal).\n- [ ] Study American Revolution Video Notes.\n- [ ] Submit on Blackboard.",
        "start_date": "06/08/2026",
        "due_date": "06/14/2026",
        "priority": 2,  # High
        "points": 50,
        "subtasks": [
            "Select 10 documents from assignment prompt groups A-E",
            "Review video notes/assignments/american_revolution_video_notes.md",
            "Draft comparative Revolution narrative",
            "Submit Major Essay Two on Blackboard"
        ]
    },
    {
        "name": "Book Essay 6: Inequality and Freedom (Horn Ch 6 & Epilogue)",
        "description": "Write a response to Horn's Chapter 6 and Epilogue regarding inequality, freedom, and the legacy of 1619.\n\n### Requirements:\n- Length: 1-2 pages.\n- Value: 25 points.\n\n### Checklist:\n- [ ] Read Horn Chapter 6 (Inequality and Freedom) and Epilogue.\n- [ ] Study Inequality & Freedom Video Notes.\n- [ ] Draft response essay.\n- [ ] Submit on Blackboard.",
        "start_date": "06/15/2026",
        "due_date": "06/19/2026",
        "priority": 3,  # Normal
        "points": 25,
        "subtasks": [
            "Read reading notes/readings/1619/chapter_06.md",
            "Read reading notes/readings/1619/epilogue.md",
            "Review video notes/assignments/inequality_and_freedom_video_notes.md",
            "Draft 1619 legacy response",
            "Submit Book Essay 6 on Blackboard"
        ]
    },
    {
        "name": "Major Essay Three: Articles vs. Constitution",
        "description": "Address power distribution, structures, and the missing Bill of Rights in a comparative essay on the Articles and U.S. Constitution.\n\n### Requirements:\n- Length: 2-3 pages.\n- Font: Times New Roman, 12pt, double-spaced.\n- Value: 50 points.\n\n### Checklist:\n- [ ] Read Articles of Confederation (1776).\n- [ ] Read The U.S. Constitution (1787).\n- [ ] Study Articles vs. Constitution Video Notes.\n- [ ] Draft essay.\n- [ ] Submit on Blackboard.",
        "start_date": "06/15/2026",
        "due_date": "06/21/2026",
        "priority": 2,  # High
        "points": 50,
        "subtasks": [
            "Read source text 'Articles of Confederation (1776)'",
            "Read source text 'Original 1787 U.S. Constitution'",
            "Review video notes/assignments/articles_vs_constitution_video_notes.md",
            "Draft comparative essay",
            "Submit Major Essay Three on Blackboard"
        ]
    },
    {
        "name": "Major Essay Four: Creation of Two Societies",
        "description": "Compare the Free Labor (North) and Slave Labor (South) systems, economies, and political structures based on Bruce Levine's book.\n\n### Requirements:\n- Length: 2-3 pages.\n- Font: Times New Roman, 12pt, double-spaced.\n- Value: 50 points.\n\n### Checklist:\n- [ ] Read Chapters 1 and 2 from Bruce Levine's book.\n- [ ] Study Creation of Two Societies Video Notes.\n- [ ] Draft comparison essay.\n- [ ] Submit on Blackboard.",
        "start_date": "06/17/2026",
        "due_date": "06/21/2026",
        "priority": 2,  # High
        "points": 50,
        "subtasks": [
            "Read Bruce Levine's Chapters 1 & 2 PDF",
            "Review video notes/assignments/creation_of_two_societies_video_notes.md",
            "Draft Free Labor vs. Slave Labor analysis",
            "Submit Major Essay Four on Blackboard"
        ]
    },
    {
        "name": "Major Essay Five: Debate over Slavery (Proslavery Ideology)",
        "description": "Explain the core beliefs and theological/social justifications of proslavery ideology in the 1830s.\n\n### Requirements:\n- Length: 2-3 pages.\n- Font: Times New Roman, 12pt, double-spaced.\n- Value: 50 points.\n\n### Checklist:\n- [ ] Read article by Jack Maddex OR Drew Gilpin Faust.\n- [ ] Study Debate over Slavery Video Notes.\n- [ ] Draft theological defense analysis.\n- [ ] Submit on Blackboard.",
        "start_date": "06/22/2026",
        "due_date": "06/26/2026",
        "priority": 2,  # High
        "points": 50,
        "subtasks": [
            "Select and read article (Maddex PDF or Faust PDF)",
            "Review video notes/assignments/debate_over_slavery_video_notes.md",
            "Draft proslavery theology response",
            "Submit Major Essay Five on Blackboard"
        ]
    },
    {
        "name": "Major Essay Six: W.E.B. Du Bois on the Civil War",
        "description": "Evaluate W.E.B. Du Bois's 1935 essay and his 'general strike' thesis regarding the causes/significance of the Civil War.\n\n### Requirements:\n- Length: 2-3 pages.\n- Font: Times New Roman, 12pt, double-spaced.\n- Value: 50 points.\n\n### Checklist:\n- [ ] Read W.E.B. Du Bois's essay.\n- [ ] Study Civil War Video Notes.\n- [ ] Draft historiographical essay.\n- [ ] Submit on Blackboard.",
        "start_date": "06/24/2026",
        "due_date": "06/29/2026",
        "priority": 2,  # High
        "points": 50,
        "subtasks": [
            "Read W.E.B. Du Bois's source PDF",
            "Review video notes/assignments/civil_war_video_notes.md",
            "Draft general strike analysis",
            "Submit Major Essay Six on Blackboard"
        ]
    }
]

def date_to_ms(date_str):
    if not date_str:
        return None
    dt = datetime.datetime.strptime(date_str, "%m/%d/%Y")
    # ClickUp prefers local-centric timestamps. 
    # Set it to 8:00 AM to avoid timezone offset changes rolling it to a previous day.
    dt = dt.replace(hour=8, minute=0, second=0, microsecond=0)
    return int(dt.timestamp() * 1000)

def clickup_api_request(url, method="GET", headers=None, data=None):
    if headers is None:
        headers = {}
    
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            if not res_data.strip():
                return {}
            return json.loads(res_data)
    except urllib.error.HTTPError as e:
        err_content = e.read().decode("utf-8")
        print(f"\n[ERROR] ClickUp API returned HTTP {e.code}: {e.reason}")
        print(f"[ERROR] Response details: {err_content}")
        raise e
    except Exception as e:
        print(f"\n[ERROR] Network error: {str(e)}")
        raise e

# List of all course markdown files to be imported
markdown_files = {
    "notes/syllabus.md": "Course Syllabus",
    "notes/modules/course_introduction_transcript.md": "Welcome Lecture Transcript",
    "notes/readings/christopher_columbus_biography.md": "Christopher Columbus Biography (Traditional)",
    "notes/readings/columbus_and_the_recovery_of_jerusalem.md": "Columbus and the Recovery of Jerusalem (Hamdani)",
    "notes/readings/1619/introduction.md": "1619 Introduction",
    "notes/readings/1619/chapter_01.md": "1619 Chapter 1 - Jamestown",
    "notes/readings/1619/chapter_02.md": "1619 Chapter 2 - The Great Reforms",
    "notes/readings/1619/chapter_03.md": "1619 Chapter 3 - First Africans",
    "notes/readings/1619/chapter_04.md": "1619 Chapter 4 - Commonwealth",
    "notes/readings/1619/chapter_05.md": "1619 Chapter 5 - Tumult and Liberty",
    "notes/readings/1619/chapter_06.md": "1619 Chapter 6 - Inequality and Freedom",
    "notes/readings/1619/epilogue.md": "1619 Epilogue",
    "notes/assignments/columbus_essay_video_notes.md": "Columbus Essay Lecture Notes",
    "notes/assignments/colonial_settlement_video_notes.md": "Colonial Settlement Lecture Notes",
    "notes/assignments/great_reforms_video_notes.md": "Great Reforms Lecture Notes",
    "notes/assignments/first_africans_video_notes.md": "First Africans Lecture Notes",
    "notes/assignments/commonwealth_video_notes.md": "Commonwealth Lecture Notes",
    "notes/assignments/tumult_and_liberty_video_notes.md": "Tumult and Liberty Lecture Notes",
    "notes/assignments/american_revolution_video_notes.md": "American Revolution Lecture Notes",
    "notes/assignments/inequality_and_freedom_video_notes.md": "Inequality and Freedom Lecture Notes",
    "notes/assignments/articles_vs_constitution_video_notes.md": "Articles vs Constitution Lecture Notes",
    "notes/assignments/creation_of_two_societies_video_notes.md": "Creation of Two Societies Lecture Notes",
    "notes/assignments/debate_over_slavery_video_notes.md": "Debate over Slavery Lecture Notes",
    "notes/assignments/civil_war_video_notes.md": "Civil War Lecture Notes"
}
import re

def find_all_markdown_files(workspace_root):
    md_files = []
    notes_path = os.path.join(workspace_root, "notes")
    for root, dirs, files in os.walk(notes_path):
        if ".venv" in root or ".git" in root or "scratch" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel = os.path.relpath(full_path, workspace_root).replace("\\", "/")
                md_files.append(rel)
    return md_files

def get_doc_title(rel_path):
    if "readings/1619/" in rel_path:
        # Custom 1619 Book page titles in chronological order
        book_titles = {
            "notes/readings/1619/preface.md": "1619: Book Overview & Preface",
            "notes/readings/1619/copyright.md": "01. Copyright & Licensing",
            "notes/readings/1619/dedication.md": "02. Dedication & Epigraph",
            "notes/readings/1619/authors_note.md": "03. Author's Note",
            "notes/readings/1619/introduction.md": "04. Introduction",
            "notes/readings/1619/chapter_01.md": "05. Chapter 1 - Jamestown",
            "notes/readings/1619/chapter_02.md": "06. Chapter 2 - The Great Reforms",
            "notes/readings/1619/chapter_03.md": "07. Chapter 3 - First Africans",
            "notes/readings/1619/chapter_04.md": "08. Chapter 4 - Commonwealth",
            "notes/readings/1619/chapter_05.md": "09. Chapter 5 - Tumult and Liberty",
            "notes/readings/1619/chapter_06.md": "10. Chapter 6 - Inequality and Freedom",
            "notes/readings/1619/epilogue.md": "11. Epilogue",
            "notes/readings/1619/acknowledgements.md": "12. Acknowledgments",
            "notes/readings/1619/about_the_author.md": "13. About the Author",
            "notes/readings/1619/endnotes.md": "14. Notes & References",
            "notes/readings/1619/book_index.md": "15. Book Index"
        }
        if rel_path in book_titles:
            return book_titles[rel_path]
        base = os.path.basename(rel_path)
        name_no_ext = os.path.splitext(base)[0]
        clean_part = name_no_ext.replace("_", " ").title()
        return f"1619 Book - {clean_part}"

    if rel_path in markdown_files:
        return markdown_files[rel_path]
    base = os.path.basename(rel_path)
    name_no_ext = os.path.splitext(base)[0]
    
    if rel_path == "notes/index.md":
        return "HIST 21103 Notes Index"
    elif rel_path == "notes/readings/1619_jamestown_and_the_founding_of_american_democracy.md":
        return "1619 Book Overview & Index"
    elif "assignments/" in rel_path and "_prompt" in rel_path:
        clean_part = name_no_ext.replace("_", " ").title()
        return f"Assignment Prompt: {clean_part}"
    else:
        return name_no_ext.replace("_", " ").title()

def get_existing_docs(workspace_id, headers):
    url = f"https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs"
    existing_docs = []
    cursor = ""
    while True:
        query_url = url
        if cursor:
            query_url += f"?cursor={cursor}"
        try:
            res = clickup_api_request(query_url, "GET", headers)
            docs = res.get("docs", res.get("documents", []))
            existing_docs.extend(docs)
            cursor = res.get("next_cursor", "")
            if not cursor:
                break
        except Exception as e:
            print(f"[!] Warning: Failed to fetch existing docs page: {str(e)}")
            break
    return existing_docs

def upload_attachment(task_id, file_path, headers):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    filename = os.path.basename(file_path)
    
    mime_type = "image/jpeg"
    if file_path.lower().endswith(".gif"):
        mime_type = "image/gif"
    elif file_path.lower().endswith(".png"):
        mime_type = "image/png"
    elif file_path.lower().endswith(".mp4"):
        mime_type = "video/mp4"
    elif file_path.lower().endswith(".m4a"):
        mime_type = "audio/mp4"
    
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()
    except Exception as e:
        print(f"[!] Warning: Failed to read asset file {file_path}: {str(e)}")
        return None
        
    part_header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="attachment"; filename="{filename}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8")
    
    part_footer = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = part_header + file_bytes + part_footer
    
    req_headers = headers.copy()
    req_headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    
    url = f"https://api.clickup.com/api/v2/task/{task_id}/attachment"
    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            return json.loads(res_data)
    except Exception as e:
        print(f"[!] Failed to upload attachment {filename}: {str(e)}")
        return None

LINK_RE = re.compile(r'(!??\[[^\]]*?\])\(([^)]*?)\)')

def rewrite_content_links(content, source_rel_path, doc_map, asset_map):
    if not source_rel_path:
        return content
    source_dir = os.path.dirname(source_rel_path)
    
    def replace_match(match):
        label = match.group(1)
        url = match.group(2).strip()
        
        if url.startswith(("http://", "https://", "mailto:", "about:")):
            return f"{label}({url})"
            
        fragment = ""
        if "#" in url:
            url_part, fragment_part = url.split("#", 1)
            url = url_part
            fragment = "#" + fragment_part
            
        if not url:
            return f"{label}({fragment})"
            
        joined = os.path.join(source_dir, url)
        canonical = os.path.normpath(joined).replace("\\", "/")
        
        matches_paths = [canonical]
        if canonical.startswith("notes/"):
            matches_paths.append(canonical.replace("notes/", "", 1))
        else:
            matches_paths.append("notes/" + canonical)
            
        matched_url = None
        for m in matches_paths:
            if m in doc_map:
                matched_url = doc_map[m]
                break
            if m in asset_map:
                matched_url = asset_map[m]
                break
                
        if matched_url:
            return f"{label}({matched_url}{fragment})"
            
        if url.endswith(".md"):
            print(f"       [!] Warning: Relative document link '{url}' in '{source_rel_path}' could not be resolved.")
        return f"{label}({url}{fragment})"
        
    return LINK_RE.sub(replace_match, content)

def determine_doc_parent(rel_path, task_id_by_name, subtask_id_by_parent_and_name, default_parent_id):
    rel_path_clean = rel_path.lower().strip()
    
    # 1. Match subtask readings
    for t in tasks_data:
        parent_name = t["name"].lower().strip()
        for st_name in t["subtasks"]:
            base_name = os.path.basename(rel_path)
            if rel_path in st_name or base_name in st_name:
                clean_st = get_clean_name(st_name).lower().strip()
                key = (parent_name, clean_st)
                if key in subtask_id_by_parent_and_name:
                    return subtask_id_by_parent_and_name[key], f"Subtask '{get_clean_name(st_name)}' under '{t['name']}'"
                    
    # 2. Match assignment prompts
    if "assignments/essay_" in rel_path_clean and "_prompt" in rel_path_clean:
        mapping = {
            "essay_01": "essay one: columbus analysis",
            "essay_02": "book essay 1: colonial settlement (horn intro & ch 1)",
            "essay_03": "book essay 2: the great reforms (horn ch 2)",
            "essay_04": "book essay 3: first Africans (horn ch 3)",
            "essay_05": "book essay 4: commonwealth (horn ch 4)",
            "essay_06": "book essay 5: tumult and liberty (horn ch 5)",
            "essay_07": "book essay 6: inequality and freedom (horn ch 6 & epilogue)",
            "essay_08": "major essay two: voices of the american revolution",
            "essay_09": "major essay three: articles vs. constitution",
            "essay_10": "major essay four: creation of two societies",
            "essay_11": "major essay five: debate over slavery (proslavery ideology)",
            "essay_12": "major essay six: w.e.b. du bois on the civil war"
        }
        for prefix, task_key in mapping.items():
            if prefix in rel_path_clean:
                if task_key in task_id_by_name:
                    return task_id_by_name[task_key], f"Parent Task '{task_key}' (Prompt)"
                    
    # 3. Specific file paths
    if rel_path_clean == "notes/index.md" or rel_path_clean == "index.md":
        key = "syllabus review & course orientation"
        if key in task_id_by_name:
            return task_id_by_name[key], "Syllabus Review Parent Task (Index)"
            
    # 4. 1619 helper docs (copyright, preface, dedication, index etc.)
    if "readings/1619/" in rel_path_clean:
        key = "book essay 1: colonial settlement (horn intro & ch 1)"
        if key in task_id_by_name:
            return task_id_by_name[key], "Book Essay 1 Task (1619 Helper)"
            
    return default_parent_id, "Default Parent Task"

def clean_markdown_text(content):
    if not content:
        return content
    # Strip frontmatter: check if the string starts with ---
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]
            
    # Clean callouts: convert lines containing > [!NOTE], etc.
    import re
    callout_re = re.compile(r'^>\s*\[!(NOTE|IMPORTANT|TIP|CAUTION|WARNING)\]', re.IGNORECASE | re.MULTILINE)
    
    def replace_callout(match):
        c_type = match.group(1).upper()
        if c_type == "NOTE":
            return "> ℹ️ **NOTE:**"
        elif c_type == "IMPORTANT":
            return "> ⚠️ **IMPORTANT:**"
        elif c_type == "TIP":
            return "> 💡 **TIP:**"
        elif c_type == "CAUTION":
            return "> ⚠️ **CAUTION:**"
        elif c_type == "WARNING":
            return "> 🛑 **WARNING:**"
        return f"> **{c_type}:**"
        
    content = callout_re.sub(replace_callout, content)
    return content.lstrip()

def classify_subtask(subtask_name):
    name_lower = subtask_name.lower()
    if any(k in name_lower for k in ["submit", "upload", "turn in", "post"]):
        return 3  # Submission phase
    elif any(k in name_lower for k in ["draft", "write", "compare", "analyze", "setup", "set up", "track", "prepare"]):
        return 2  # Drafting phase
    else:
        return 1  # Reading/Research phase (default)

def calculate_subtask_dates(parent_start_str, parent_due_str, subtasks):
    import datetime
    
    start_dt = datetime.datetime.strptime(parent_start_str, "%m/%d/%Y")
    due_dt = datetime.datetime.strptime(parent_due_str, "%m/%d/%Y")
    
    duration = (due_dt - start_dt).days + 1
    
    subtask_dates = []
    
    if duration <= 1:
        for st in subtasks:
            subtask_dates.append((parent_start_str, parent_due_str))
        return subtask_dates
        
    classified = [classify_subtask(st) for st in subtasks]
    has_submission = 3 in classified
    
    for idx, phase in enumerate(classified):
        if phase == 1:
            st_start = start_dt
            # Reading phase: take up to 50% of the duration (rounded up, min 1)
            days_to_add = max(1, int(duration * 0.5))
            st_due = start_dt + datetime.timedelta(days=days_to_add)
            if st_due >= due_dt:
                st_due = due_dt - datetime.timedelta(days=1)
        elif phase == 2:
            # Drafting phase starts around 40% of duration
            days_to_start = max(1, int(duration * 0.4))
            st_start = start_dt + datetime.timedelta(days=days_to_start)
            # If there's a submission subtask, draft is due 1 day before due_dt
            if has_submission:
                st_due = due_dt - datetime.timedelta(days=1)
            else:
                st_due = due_dt
            if st_due < st_start:
                st_due = st_start
        else:
            # Submission phase
            st_start = due_dt - datetime.timedelta(days=1)
            st_due = due_dt
            if st_start < start_dt:
                st_start = start_dt
                
        subtask_dates.append((
            st_start.strftime("%m/%d/%Y"),
            st_due.strftime("%m/%d/%Y")
        ))
        
    return subtask_dates

def get_all_doc_maps(workspace_id, headers, workspace_root, task_id_by_name, subtask_id_by_parent_and_name, default_parent_id):
    existing_docs = get_existing_docs(workspace_id, headers)
    md_files = find_all_markdown_files(workspace_root)
    
    doc_map = {}
    doc_id_map = {}
    doc_page_id_map = {}
    
    # 1. Handle the Unified 1619 Book Document
    book_doc_title = "1619: Jamestown and the Forging of American Democracy"
    book_parent_id = task_id_by_name.get("book essay 1: colonial settlement (horn intro & ch 1)", default_parent_id)
    
    book_doc_id = None
    for d in existing_docs:
        if d.get("name") and d["name"].lower().strip() == book_doc_title.lower().strip():
            d_parent = d.get("parent", {})
            d_parent_id = d_parent.get("id") if d_parent else None
            if d_parent_id == book_parent_id:
                book_doc_id = d["id"]
                break
                
    if book_doc_id:
        print(f"[+] Found existing Unified 1619 Book Document (ID: {book_doc_id})")
    else:
        print(f"[+] Unified 1619 Book Document not found. Creating parented to Book Essay 1 Task...")
        url = f"https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs"
        try:
            payload = {
                "name": book_doc_title,
                "parent": {
                    "id": book_parent_id,
                    "type": 1
                },
                "create_page": True
            }
            res = clickup_api_request(url, "POST", headers, payload)
            book_doc_id = res.get("id")
            print(f"       [+] Created Unified Book Doc (ID: {book_doc_id})")
        except Exception as e:
            print(f"       [!] Error creating Unified Book Doc: {str(e)}")
            raise e
            
    # Fetch all pages of the 1619 Book Document
    book_pages = []
    if book_doc_id:
        pages_url = f"https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{book_doc_id}/pages"
        try:
            res = clickup_api_request(pages_url, "GET", headers)
            if isinstance(res, list):
                book_pages = res
            elif isinstance(res, dict) and "pages" in res:
                book_pages = res["pages"]
        except Exception as e:
            print(f"       [!] Warning: Failed to fetch pages for 1619 Book Doc: {str(e)}")
            
    # The default first page will be renamed to "1619: Book Overview & Preface"
    parent_page_id = None
    if len(book_pages) > 0:
        parent_page_id = book_pages[0]["id"]
        print(f"[+] Parent page ID for 1619 Book Doc: {parent_page_id}")
    else:
        # If no page exists, create one
        print("[!] No pages found in Book Doc. Creating parent page...")
        pages_url = f"https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{book_doc_id}/pages"
        try:
            res = clickup_api_request(pages_url, "POST", headers, {
                "name": "1619: Book Overview & Preface",
                "content": "",
                "content_format": "text/md"
            })
            parent_page_id = res.get("id")
        except Exception as e:
            print(f"       [!] Error creating parent page: {str(e)}")
            raise e

    book_order = [
        "notes/readings/1619/preface.md",
        "notes/readings/1619/copyright.md",
        "notes/readings/1619/dedication.md",
        "notes/readings/1619/authors_note.md",
        "notes/readings/1619/introduction.md",
        "notes/readings/1619/chapter_01.md",
        "notes/readings/1619/chapter_02.md",
        "notes/readings/1619/chapter_03.md",
        "notes/readings/1619/chapter_04.md",
        "notes/readings/1619/chapter_05.md",
        "notes/readings/1619/chapter_06.md",
        "notes/readings/1619/epilogue.md",
        "notes/readings/1619/acknowledgements.md",
        "notes/readings/1619/about_the_author.md",
        "notes/readings/1619/endnotes.md",
        "notes/readings/1619/book_index.md"
    ]
    
    other_files = [f for f in md_files if "readings/1619/" not in f]
    book_files_in_md = [f for f in md_files if "readings/1619/" in f]
    
    sorted_book_files = []
    for path in book_order:
        if path in book_files_in_md:
            sorted_book_files.append(path)
            book_files_in_md.remove(path)
    sorted_book_files.extend(book_files_in_md)
    
    ordered_md_files = other_files + sorted_book_files

    print(f"\n[~] Scanning and syncing {len(ordered_md_files)} Task-bound ClickUp Documents...")
    for rel_path in ordered_md_files:
        clean_title = get_doc_title(rel_path)
        
        # Check if this file belongs to the 1619 Book
        if "readings/1619/" in rel_path:
            # It's a 1619 Book subpage
            doc_id = book_doc_id
            page_id = None
            
            # Special Case: Preface is mapped directly to the parent page
            if rel_path.endswith("preface.md"):
                page_id = parent_page_id
                print(f"    -> Mapping '{clean_title}' to parent page (ID: {page_id}).")
            else:
                # Match page by title inside book_pages
                for p in book_pages:
                    if p.get("name") and p["name"].lower().strip() == clean_title.lower().strip():
                        page_id = p["id"]
                        break
                        
                if page_id:
                    print(f"    -> Subpage '{clean_title}' already exists in Book Document (Page ID: {page_id}).")
                else:
                    print(f"    -> Subpage '{clean_title}' not found. Creating nested subpage...")
                    pages_url = f"https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{book_doc_id}/pages"
                    try:
                        payload = {
                            "name": clean_title,
                            "parent_page_id": parent_page_id,
                            "content": "",
                            "content_format": "text/md"
                        }
                        res = clickup_api_request(pages_url, "POST", headers, payload)
                        page_id = res.get("id")
                        print(f"       [+] Created Subpage (Page ID: {page_id})")
                        book_pages.append({"id": page_id, "name": clean_title})
                    except Exception as e:
                        print(f"       [!] Error creating Subpage '{clean_title}': {str(e)}")
                        continue
            
            if page_id:
                doc_url = f"https://app.clickup.com/{workspace_id}/v/dc/{book_doc_id}/p/{page_id}"
                doc_map[rel_path] = doc_url
                doc_id_map[rel_path] = book_doc_id
                doc_page_id_map[rel_path] = page_id
                
        else:
            # Standalone Document
            parent_id, parent_desc = determine_doc_parent(
                rel_path, task_id_by_name, subtask_id_by_parent_and_name, default_parent_id
            )
            
            # Match by name AND parent_id
            doc_id = None
            for d in existing_docs:
                if d.get("name") and d["name"].lower().strip() == clean_title.lower().strip():
                    d_parent = d.get("parent", {})
                    d_parent_id = d_parent.get("id") if d_parent else None
                    if d_parent_id == parent_id:
                        doc_id = d["id"]
                        break
                        
            if doc_id:
                print(f"    -> Doc '{clean_title}' already exists parented to {parent_desc} (ID: {doc_id}).")
            else:
                print(f"    -> Doc '{clean_title}' not found. Creating parented to {parent_desc}...")
                url = f"https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs"
                try:
                    payload = {
                        "name": clean_title,
                        "parent": {
                            "id": parent_id,
                            "type": 1
                        },
                        "create_page": True
                    }
                    res = clickup_api_request(url, "POST", headers, payload)
                    doc_id = res.get("id")
                    print(f"       [+] Created Doc (ID: {doc_id})")
                except Exception as e:
                    print(f"       [!] Error creating Doc '{clean_title}': {str(e)}")
                    continue
                    
            if doc_id:
                # Standalone Doc default page ID query
                page_id = None
                pages_url = f"https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}/pages"
                try:
                    res = clickup_api_request(pages_url, "GET", headers)
                    if isinstance(res, list) and len(res) > 0:
                        page_id = res[0]["id"]
                    elif isinstance(res, dict) and "pages" in res and len(res["pages"]) > 0:
                        page_id = res["pages"][0]["id"]
                except Exception as e:
                    pass
                
                doc_url = f"https://app.clickup.com/{workspace_id}/v/dc/{doc_id}"
                doc_map[rel_path] = doc_url
                doc_id_map[rel_path] = doc_id
                if page_id:
                    doc_page_id_map[rel_path] = page_id
                else:
                    doc_page_id_map[rel_path] = f"first_page_of_{doc_id}"
                    
    return md_files, doc_map, doc_id_map, doc_page_id_map

def update_clickup_doc_pages(workspace_id, headers, workspace_root, md_files, doc_id_map, doc_page_id_map, doc_map, asset_map):
    print(f"\n[~] Updating content for {len(doc_page_id_map)} Document pages...")
    for rel_path, page_id in doc_page_id_map.items():
        doc_id = doc_id_map[rel_path]
        clean_title = get_doc_title(rel_path)
        full_path = os.path.join(workspace_root, rel_path)
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = clean_markdown_text(f.read())
        except Exception as e:
            print(f"    [!] Error reading file '{rel_path}': {str(e)}")
            continue
            
        rewritten_content = rewrite_content_links(content, rel_path, doc_map, asset_map)
        
        # If it's a 1619 preface, we also rename the parent page to the clean preface title
        page_name_to_use = clean_title
        if rel_path.endswith("preface.md"):
            page_name_to_use = "1619: Book Overview & Preface"
            
        if page_id.startswith("first_page_of_"):
            actual_doc_id = page_id.replace("first_page_of_", "")
            pages_url = f"https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{actual_doc_id}/pages"
            try:
                pages = clickup_api_request(pages_url, "GET", headers)
                actual_page_id = None
                if isinstance(pages, list) and len(pages) > 0:
                    actual_page_id = pages[0]["id"]
                elif isinstance(pages, dict) and "pages" in pages and len(pages["pages"]) > 0:
                    actual_page_id = pages["pages"][0]["id"]
                
                if actual_page_id:
                    page_url = f"{pages_url}/{actual_page_id}"
                    print(f"    -> Updating page for '{clean_title}' (Page ID: {actual_page_id})...")
                    clickup_api_request(page_url, "PUT", headers, {
                        "name": page_name_to_use,
                        "content": rewritten_content,
                        "content_format": "text/md"
                    })
            except Exception as e:
                print(f"    [!] Error in fallback page update: {str(e)}")
        else:
            pages_url = f"https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}/pages"
            page_url = f"{pages_url}/{page_id}"
            print(f"    -> Updating page for '{clean_title}' (Page ID: {page_id})...")
            try:
                clickup_api_request(page_url, "PUT", headers, {
                    "name": page_name_to_use,
                    "content": rewritten_content,
                    "content_format": "text/md"
                })
            except Exception as e:
                print(f"    [!] Error updating page content for page '{clean_title}': {str(e)}")

def scan_and_upload_assets(workspace_root, md_files, workspace_id, headers, default_task_id, existing_parents):
    print("\n[~] Scanning course materials for relative asset links (images, media)...")
    
    asset_paths = set()
    for rel_path in md_files:
        full_path = os.path.join(workspace_root, rel_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            matches = LINK_RE.findall(content)
            source_dir = os.path.dirname(rel_path)
            for label, url in matches:
                url = url.strip()
                if not url.startswith(("http://", "https://", "mailto:", "about:")):
                    if "#" in url:
                        url = url.split("#", 1)[0]
                    if not url:
                        continue
                    if not url.endswith(".md"):
                        joined = os.path.join(source_dir, url)
                        canonical = os.path.normpath(joined).replace("\\", "/")
                        asset_paths.add(canonical)
        except Exception as e:
            pass
            
    print(f"[+] Found {len(asset_paths)} unique non-markdown relative asset links.")
    
    asset_map = {}
    for asset in sorted(asset_paths):
        full_asset_path = os.path.join(workspace_root, asset)
        
        if not os.path.exists(full_asset_path):
            if asset.startswith("notes/"):
                alt_asset = asset.replace("notes/", "", 1)
            else:
                alt_asset = "notes/" + asset
            alt_path = os.path.join(workspace_root, alt_asset)
            if os.path.exists(alt_path):
                asset = alt_asset
                full_asset_path = alt_path
                
        if not os.path.exists(full_asset_path):
            print(f"    [!] Asset file '{asset}' does not exist on disk. Skipping.")
            continue
            
        upload_task_id = default_task_id
        asset_lower = asset.lower()
        if "columbus" in asset_lower:
            key = "essay one: columbus analysis"
            if key in existing_parents:
                upload_task_id = existing_parents[key]["id"]
        elif "settlement" in asset_lower or "colonial" in asset_lower:
            key = "book essay 1: colonial settlement (horn intro & ch 1)"
            if key in existing_parents:
                upload_task_id = existing_parents[key]["id"]
                
        print(f"    -> Uploading asset '{asset}' to task ID: {upload_task_id}...")
        res = upload_attachment(upload_task_id, full_asset_path, headers)
        if res and "url" in res:
            asset_map[asset] = res["url"]
            if asset.startswith("notes/"):
                asset_map[asset.replace("notes/", "", 1)] = res["url"]
            else:
                asset_map["notes/" + asset] = res["url"]
            print(f"       [+] Uploaded successfully. ClickUp URL: {res['url']}")
        else:
            print(f"       [!] Failed to upload asset '{asset}'.")
            
    return asset_map

def get_clean_name(name):
    for path, clean in markdown_files.items():
        if path in name or os.path.basename(path) in name:
            action = "Read" if "read" in name.lower() else "Review"
            return f"{action}: {clean}"
    return name

def get_subtask_markdown(st_name, parent_task_name):
    clean_name = get_clean_name(st_name)
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if there is a corresponding file path
    matched_path = None
    for rel_path in markdown_files.keys():
        base_name = os.path.basename(rel_path)
        if rel_path in st_name or base_name in st_name:
            matched_path = os.path.join(workspace_root, rel_path)
            break
            
    file_content = ""
    if matched_path and os.path.exists(matched_path):
        try:
            with open(matched_path, "r", encoding="utf-8") as f:
                file_content = clean_markdown_text(f.read())
        except Exception as e:
            print(f"[!] Warning: Failed to read file {matched_path}: {str(e)}")
            
    # Subtask checklists
    checklist = []
    st_lower = st_name.lower()
    description = ""
    
    if matched_path:
        # It's a reading task
        description = f"### Full Reading Content:\n---\n{file_content}\n---\n" if file_content else ""
        checklist = [
            f"Read the embedded text for {clean_name}",
            "Highlight key arguments, dates, and historical figures",
            "Select specific quotes/citations to support your essay"
        ]
    elif "select 10 documents" in st_lower:
        description = "Select exactly 10 primary source documents (2 from each group A through E) to compare and contrast for Major Essay Two."
        checklist = [
            "Select 2 documents from Group A (Religious)",
            "Select 2 documents from Group B (Loyalist)",
            "Select 2 documents from Group C (Rebel)",
            "Select 2 documents from Group D (African American)",
            "Select 2 documents from Group E (Official/Legal)",
            "Ensure you have exactly 10 documents selected before starting to write"
        ]
    elif st_lower.startswith("draft ") or st_lower.startswith("write "):
        description = f"Draft the essay for **{parent_task_name}** according to the professor's prompt requirements."
        checklist = [
            "Outline the essay structure (Introduction, Body Paragraphs, Conclusion)",
            "Draft an introduction with a strong, arguable thesis statement",
            "Write the body paragraphs, ensuring each paragraph starts with a clear topic sentence",
            "Integrate direct quotes and specific evidence from the required readings",
            "Ensure citations are formatted correctly (e.g., standard page number citations)",
            "Write a conclusion that summarizes the main argument and reflects on the broader historical significance"
        ]
    elif st_lower.startswith("submit ") or st_lower.startswith("upload "):
        description = f"Submit your final draft of **{parent_task_name}** to the course Blackboard portal."
        checklist = [
            "Perform a final proofreading pass (check spelling, grammar, and sentence structure)",
            "Verify formatting: Times New Roman, 12pt, double-spaced (check page limits in prompt)",
            "Export the document as a PDF or DOCX file",
            "Log into the Blackboard portal and navigate to the assignment submission page",
            "Upload the file and click Submit",
            "Verify that you receive a submission receipt or confirmation email"
        ]
    elif "clickup" in st_lower:
        description = "Set up your ClickUp list, milestones, statuses, and custom fields to keep your progress tracked throughout the 5-week course."
        checklist = [
            "Ensure all 13 major tasks are imported successfully",
            "Double-check due dates and start dates against the course syllabus",
            "Create a custom number field called 'Points' to track your grade points",
            "Familiarize yourself with the task checklists and descriptions"
        ]
    else:
        description = f"Complete the subtask: **{st_name}** for **{parent_task_name}**."
        checklist = [
            f"Review the requirements for {st_name}",
            "Perform necessary research or preparation",
            "Mark as complete when finished"
        ]
        
    # Format checklist as ClickUp Markdown checkboxes
    markdown_checklist = "\n\n### Subtask Checklist:\n" + "\n".join([f"- [ ] {item}" for item in checklist])
    return f"# {clean_name}\n\n{description}{markdown_checklist}"

def clean_parent_description(desc):
    if not desc:
        return desc
    # Replace file paths with simple text names
    for rel_path, clean_name in markdown_files.items():
        base_name = os.path.basename(rel_path)
        paths_to_replace = [
            rel_path,
            rel_path.replace("notes/", ""),
            "../" + rel_path.replace("notes/", ""),
            "./" + rel_path.replace("notes/assignments/", ""),
            "notes/readings/" + base_name,
            "readings/" + base_name,
            base_name
        ]
        for p in paths_to_replace:
            if p in desc:
                desc = desc.replace(p, f"**{clean_name}**")
    return desc

def clear_list_tasks(list_id, headers, force=False):
    if not force:
        return
        
    print("\n[~] Fetching existing tasks to clear...")
    # Fetch all tasks in the list (including subtasks)
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task?subtasks=true"
    tasks_data = clickup_api_request(url, "GET", headers)
    tasks = tasks_data.get("tasks", [])
    
    # We only need to delete parent tasks (deleting a parent automatically deletes its subtasks in ClickUp)
    parent_tasks = [t for t in tasks if t.get("parent") is None]
    
    if not parent_tasks:
        print("[+] List is already empty. No tasks to clear.")
        return
        
    print(f"[!] Found {len(parent_tasks)} parent tasks in ClickUp list.")
    confirm = input("Are you sure you want to delete all existing tasks in this list? (y/n): ").strip().lower()
    if confirm != 'y':
        print("[~] Skipping clearing. Proceeding with import...")
        return
        
    print(f"[~] Deleting {len(parent_tasks)} parent tasks (and their subtasks)...")
    for t in parent_tasks:
        print(f"    -> Deleting task: '{t['name']}' (ID: {t['id']})...")
        delete_url = f"https://api.clickup.com/api/v2/task/{t['id']}"
        clickup_api_request(delete_url, "DELETE", headers)
        
    print("[+] List cleared successfully!\n")

def main():
    print("====================================================")
    print("         HIST 21103 ClickUp Tasks Importer          ")
    print("====================================================\n")
    
    # Check for CLI flags
    force_clear = "--clear" in sys.argv or "-c" in sys.argv
    non_interactive = "--non-interactive" in sys.argv or "-n" in sys.argv or force_clear
    
    # 1. Gather Token and List ID (with defaults)
    default_token = "pk_57181843_7A77LBOH1UJUQS9EPJUH1IOOL62WY4CA"
    default_list_id = "901113816940"
    
    if non_interactive:
        print("[~] Running in non-interactive mode. Using default credentials.")
        api_token = default_token
        list_id = default_list_id
    else:
        api_token = input(f"Please paste your ClickUp Personal API Token [Default: {default_token[:6]}...{default_token[-6:]}]: ").strip()
        if not api_token:
            api_token = default_token
            
        list_id = input(f"Please enter your target ClickUp List ID [Default: {default_list_id}]: ").strip()
        if not list_id:
            list_id = default_list_id
        
    headers = {
        "Authorization": api_token
    }
    
    # 2. Fetch list details to extract workspace_id (team_id)
    # 2. Fetch list details and workspaces to extract workspace_id (team_id)
    print("\n[~] Connecting to ClickUp & fetching list information...")
    try:
        # Check list access
        list_url = f"https://api.clickup.com/api/v2/list/{list_id}"
        list_data = clickup_api_request(list_url, "GET", headers)
        
        # Get workspaces
        teams_url = "https://api.clickup.com/api/v2/team"
        teams_data = clickup_api_request(teams_url, "GET", headers)
        teams = teams_data.get("teams", [])
        if len(teams) > 0:
            workspace_id = teams[0].get("id")
        else:
            workspace_id = None
            
        print(f"[+] Connected successfully. Workspace ID: {workspace_id}")
        if not workspace_id:
            print("[ERROR] Workspace ID could not be found.")
            sys.exit(1)
    except Exception as e:
        print("[ERROR] Connection verification failed. Please double-check your API token and List ID.")
        sys.exit(1)
        
    # Get Custom Fields
    try:
        fields_url = f"https://api.clickup.com/api/v2/list/{list_id}/field"
        fields_data = clickup_api_request(fields_url, "GET", headers)
        
        points_field_id = None
        for field in fields_data.get("fields", []):
            if field.get("name", "").lower() in ["points", "points planned", "grade points"]:
                points_field_id = field.get("id")
                print(f"[+] Found custom field: '{field.get('name')}' (ID: {points_field_id})")
                break
                
        if not points_field_id:
            print("[!] Note: No custom field named 'Points' or 'Points Planned' was found.")
            print("    If you want the script to upload points, add a custom number field named 'Points' to the list first.")
            print("    The script will continue and skip points uploads.")
            
    except Exception as e:
        print(f"[!] Warning: Failed to fetch custom fields: {str(e)}")
        points_field_id = None
        
    # Clear List ONLY if user explicitly passed --clear flag
    if force_clear:
        try:
            clear_list_tasks(list_id, headers, force=force_clear)
        except Exception as e:
            print(f"[!] Warning: Failed to clear list tasks: {str(e)}")
            print("    Proceeding with import anyway...")
            
    # 3. Retrieve all existing tasks in ClickUp list to match in-place
    print("\n[~] Querying existing tasks for in-place matching...")
    try:
        tasks_url = f"https://api.clickup.com/api/v2/list/{list_id}/task?subtasks=true"
        existing_data = clickup_api_request(tasks_url, "GET", headers)
        all_existing = existing_data.get("tasks", [])
        
        parent_tasks_list = [t for t in all_existing if t.get("parent") is None]
        subtasks_list = [t for t in all_existing if t.get("parent") is not None]
        
        existing_parents = {t["name"].lower().strip(): t for t in parent_tasks_list if t.get("name")}
        
        existing_subtasks_by_parent = {}
        for t in subtasks_list:
            parent_info = t["parent"]
            parent_id = parent_info if isinstance(parent_info, str) else parent_info.get("id")
            if parent_id not in existing_subtasks_by_parent:
                existing_subtasks_by_parent[parent_id] = []
            existing_subtasks_by_parent[parent_id].append(t)
            
        print(f"[+] Loaded {len(parent_tasks_list)} parent tasks and {len(subtasks_list)} subtasks from ClickUp.")
    except Exception as e:
        print(f"[ERROR] Failed to query existing tasks: {str(e)}")
        sys.exit(1)
        
    # 4. PASS 1: Synchronize all parent tasks and subtasks in ClickUp
    # This loop establishes the tasks and subtasks first and records their IDs
    print(f"\n[~] PASS 1: Synchronizing all ClickUp tasks and subtasks in-place...\n")
    
    task_id_by_name = {}
    subtask_id_by_parent_and_name = {}
    
    for i, t in enumerate(tasks_data, 1):
        task_name = t["name"]
        print(f"[{i}/{len(tasks_data)}] PASS 1: Syncing task: '{task_name}'...")
        
        # We update/create tasks with their raw clean description (without link rewriting yet)
        parent_description = clean_parent_description(t["description"])
        
        start_ms = date_to_ms(t["start_date"])
        due_ms = date_to_ms(t["due_date"])
        
        parent_key = task_name.lower().strip()
        parent_task_id = None
        
        task_payload = {
            "name": task_name,
            "markdown_content": parent_description,
            "start_date": start_ms,
            "due_date": due_ms,
            "priority": t["priority"]
        }
        
        try:
            # Check if parent task already exists
            if parent_key in existing_parents:
                parent_task_id = existing_parents[parent_key]["id"]
                print(f"    -> Parent task exists (ID: {parent_task_id}). Updating fields...")
                task_url = f"https://api.clickup.com/api/v2/task/{parent_task_id}"
                clickup_api_request(task_url, "PUT", headers, task_payload)
            else:
                print("    -> Parent task not found. Creating a new one...")
                task_url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
                res = clickup_api_request(task_url, "POST", headers, task_payload)
                parent_task_id = res.get("id")
                print(f"    -> Created Parent Task (ID: {parent_task_id})")
                
            task_id_by_name[parent_key] = parent_task_id
            
            # Update Points if Custom Field matches and points > 0
            if points_field_id and t["points"] > 0:
                print(f"    -> Updating points custom field to {t['points']}...")
                cf_url = f"https://api.clickup.com/api/v2/task/{parent_task_id}/field/{points_field_id}"
                clickup_api_request(cf_url, "POST", headers, {"value": t["points"]})
                
            # Fetch existing subtasks under this parent task
            current_subtasks = existing_subtasks_by_parent.get(parent_task_id, [])
            
            # Calculate subtask dates
            subtask_dates_list = calculate_subtask_dates(t["start_date"], t["due_date"], t["subtasks"])
            
            # Sync each required subtask
            for idx, st_name in enumerate(t["subtasks"]):
                clean_st_name = get_clean_name(st_name)
                st_desc = get_subtask_markdown(st_name, task_name)
                
                st_start_str, st_due_str = subtask_dates_list[idx]
                st_start_ms = date_to_ms(st_start_str)
                st_due_ms = date_to_ms(st_due_str)
                
                # Match existing subtask
                matched_st = None
                for est in current_subtasks:
                    est_name = est.get("name")
                    if not est_name:
                        continue
                    est_name_lower = est_name.lower().strip()
                    if est_name_lower == clean_st_name.lower().strip() or est_name_lower == st_name.lower().strip():
                        matched_st = est
                        break
                    for rel_path in markdown_files.keys():
                        base = os.path.basename(rel_path).lower()
                        if base in est_name_lower and base in st_name.lower():
                            matched_st = est
                            break
                    if matched_st:
                        break
                        
                subtask_id = None
                if matched_st:
                    subtask_id = matched_st["id"]
                    print(f"       [*] Updating existing subtask: '{clean_st_name}' (ID: {subtask_id}) [Start: {st_start_str}, Due: {st_due_str}]...")
                    sub_url = f"https://api.clickup.com/api/v2/task/{subtask_id}"
                    clickup_api_request(sub_url, "PUT", headers, {
                        "name": clean_st_name,
                        "markdown_content": st_desc,
                        "start_date": st_start_ms,
                        "due_date": st_due_ms
                    })
                else:
                    print(f"       [+] Creating new subtask: '{clean_st_name}' [Start: {st_start_str}, Due: {st_due_str}]...")
                    create_url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
                    res = clickup_api_request(create_url, "POST", headers, {
                        "name": clean_st_name,
                        "parent": parent_task_id,
                        "markdown_content": st_desc,
                        "start_date": st_start_ms,
                        "due_date": st_due_ms
                    })
                    subtask_id = res.get("id")
                    
                if subtask_id:
                    key = (parent_key, clean_st_name.lower().strip())
                    subtask_id_by_parent_and_name[key] = subtask_id
                    
            print("    -> Done!\n")
            
        except Exception as e:
            print(f"\n[ERROR] Failed to sync task '{task_name}' in Pass 1. Aborting.")
            raise e

    # Determine default parent task ID for Documents
    default_task_id = list(task_id_by_name.values())[0]

    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 5. PASS 2: Fetch/Create TASK-BOUND Documents and build URL maps
    md_files, doc_map, doc_id_map, doc_page_id_map = get_all_doc_maps(
        workspace_id, headers, workspace_root, task_id_by_name, subtask_id_by_parent_and_name, default_task_id
    )
    
    # 6. PASS 2.5: Upload non-markdown assets and build URL maps
    asset_map = scan_and_upload_assets(workspace_root, md_files, workspace_id, headers, default_task_id, existing_parents)
    
    # 7. PASS 2.9: Update ClickUp Document page contents with rewritten links
    update_clickup_doc_pages(workspace_id, headers, workspace_root, md_files, doc_id_map, doc_page_id_map, doc_map, asset_map)
    
    # 8. PASS 3: Rewrite and Update ClickUp Task & Subtask descriptions in-place
    print(f"\n[~] PASS 3: Updating ClickUp task and subtask descriptions with rewritten links...\n")
    
    for i, t in enumerate(tasks_data, 1):
        task_name = t["name"]
        parent_key = task_name.lower().strip()
        parent_task_id = task_id_by_name.get(parent_key)
        
        if not parent_task_id:
            continue
            
        print(f"[{i}/{len(tasks_data)}] PASS 3: Updating task descriptions: '{task_name}'...")
        
        # Rewrite parent description links
        parent_description_cleaned = clean_parent_description(t["description"])
        parent_description = rewrite_content_links(parent_description_cleaned, "notes/syllabus.md", doc_map, asset_map)
        
        try:
            task_url = f"https://api.clickup.com/api/v2/task/{parent_task_id}"
            clickup_api_request(task_url, "PUT", headers, {"markdown_content": parent_description})
            
            # Update subtasks
            for st_name in t["subtasks"]:
                clean_st_name = get_clean_name(st_name)
                st_desc = get_subtask_markdown(st_name, task_name)
                
                matched_rel_path = None
                for rel_path in markdown_files.keys():
                    base_name = os.path.basename(rel_path)
                    if rel_path in st_name or base_name in st_name:
                        matched_rel_path = rel_path
                        break
                        
                st_desc_rewritten = rewrite_content_links(st_desc, matched_rel_path, doc_map, asset_map)
                
                key = (parent_key, clean_st_name.lower().strip())
                sub_id = subtask_id_by_parent_and_name.get(key)
                if sub_id:
                    sub_url = f"https://api.clickup.com/api/v2/task/{sub_id}"
                    clickup_api_request(sub_url, "PUT", headers, {"markdown_content": st_desc_rewritten})
                    
            print("    -> Done!\n")
        except Exception as e:
            print(f"[!] Warning: Failed to update description in Pass 3: {str(e)}")
            
    print("\n====================================================")
    print("    SUCCESS! ClickUp tasks synchronized in-place!    ")
    print("====================================================")

if __name__ == "__main__":
    main()

