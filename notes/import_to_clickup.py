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
                file_content = f.read()
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
    print("\n[~] Connecting to ClickUp & fetching list information...")
    try:
        list_url = f"https://api.clickup.com/api/v2/list/{list_id}"
        list_data = clickup_api_request(list_url, "GET", headers)
        workspace_id = list_data.get("team_id")
        print(f"[+] Connected successfully. Workspace ID: {workspace_id}")
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
        
        existing_parents = {t["name"].lower().strip(): t for t in parent_tasks_list}
        
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
        
    # 4. Synchronize Tasks Loop
    print(f"\n[~] Beginning in-place synchronization of {len(tasks_data)} assignments...\n")
    
    for i, t in enumerate(tasks_data, 1):
        task_name = t["name"]
        print(f"[{i}/{len(tasks_data)}] Syncing task: '{task_name}'...")
        
        # Clean parent description
        parent_description = clean_parent_description(t["description"])
        
        start_ms = date_to_ms(t["start_date"])
        due_ms = date_to_ms(t["due_date"])
        
        parent_key = task_name.lower().strip()
        parent_task_id = None
        
        # Prepare task payload
        task_payload = {
            "name": task_name,
            "markdown_content": parent_description,
            "start_date": start_ms,
            "due_date": due_ms,
            "priority": t["priority"]
        }
        
        try:
            # Check if parent task already exists in ClickUp
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
                
            # Update Points if Custom Field matches and points > 0
            if points_field_id and t["points"] > 0:
                print(f"    -> Updating points custom field to {t['points']}...")
                cf_url = f"https://api.clickup.com/api/v2/task/{parent_task_id}/field/{points_field_id}"
                clickup_api_request(cf_url, "POST", headers, {"value": t["points"]})
                
            # Fetch existing subtasks under this parent task
            current_subtasks = existing_subtasks_by_parent.get(parent_task_id, [])
            
            # Sync each required subtask
            for st_name in t["subtasks"]:
                clean_st_name = get_clean_name(st_name)
                st_desc = get_subtask_markdown(st_name, task_name)
                
                # Try to find matching existing subtask
                matched_st = None
                for est in current_subtasks:
                    est_name_lower = est["name"].lower().strip()
                    # Match by exact clean name, raw name, or if a base filename matches both
                    if est_name_lower == clean_st_name.lower().strip() or est_name_lower == st_name.lower().strip():
                        matched_st = est
                        break
                    # Backup match: check if a unique base filename matches (e.g. syllabus.md)
                    for rel_path in markdown_files.keys():
                        base = os.path.basename(rel_path).lower()
                        if base in est_name_lower and base in st_name.lower():
                            matched_st = est
                            break
                    if matched_st:
                        break
                        
                # Update or create the subtask
                if matched_st:
                    sub_id = matched_st["id"]
                    print(f"       [*] Updating existing subtask: '{clean_st_name}' (ID: {sub_id})...")
                    sub_url = f"https://api.clickup.com/api/v2/task/{sub_id}"
                    clickup_api_request(sub_url, "PUT", headers, {
                        "name": clean_st_name,
                        "markdown_content": st_desc
                    })
                else:
                    print(f"       [+] Creating new subtask: '{clean_st_name}'...")
                    create_url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
                    clickup_api_request(create_url, "POST", headers, {
                        "name": clean_st_name,
                        "parent": parent_task_id,
                        "markdown_content": st_desc
                    })
                    
            print("    -> Done!\n")
            
        except Exception as e:
            print(f"\n[ERROR] Failed to sync task '{task_name}' due to an error. Aborting execution.")
            raise e
            
    print("\n====================================================")
    print("    SUCCESS! ClickUp tasks synchronized in-place!    ")
    print("====================================================")

if __name__ == "__main__":
    main()

