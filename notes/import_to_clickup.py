#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import datetime
import sys

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
            return json.loads(res_data)
    except urllib.error.HTTPError as e:
        err_content = e.read().decode("utf-8")
        print(f"\n[ERROR] ClickUp API returned HTTP {e.code}: {e.reason}")
        print(f"[ERROR] Response details: {err_content}")
        raise e
    except Exception as e:
        print(f"\n[ERROR] Network error: {str(e)}")
        raise e

def main():
    print("====================================================")
    print("         HIST 21103 ClickUp Tasks Importer          ")
    print("====================================================\n")
    
    # 1. Gather Token and List ID (with defaults)
    default_token = "pk_57181843_7A77LBOH1UJUQS9EPJUH1IOOL62WY4CA"
    default_list_id = "901113816940"
    
    api_token = input(f"Please paste your ClickUp Personal API Token [Default: {default_token[:6]}...{default_token[-6:]}]: ").strip()
    if not api_token:
        api_token = default_token
        
    list_id = input(f"Please enter your target ClickUp List ID [Default: {default_list_id}]: ").strip()
    if not list_id:
        list_id = default_list_id
        
    headers = {
        "Authorization": api_token
    }
    
    # 2. Test Connection and Get Custom Fields
    print("\n[~] Connecting to ClickUp & fetching list information...")
    try:
        # Get List Fields to find "Points" custom field ID
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
        print("[ERROR] Connection verification failed. Please double-check your API token and List ID.")
        sys.exit(1)
        
    # 3. Create Tasks Loop
    print(f"\n[~] Ready to create {len(tasks_data)} parent tasks & their subtasks. Beginning import...\n")
    
    for i, t in enumerate(tasks_data, 1):
        print(f"[{i}/{len(tasks_data)}] Creating task: '{t['name']}'...")
        
        # Prepare task payload (omitted 'status' to let ClickUp default to the list open status)
        task_payload = {
            "name": t["name"],
            "markdown_content": t["description"],
            "start_date": date_to_ms(t["start_date"]),
            "due_date": date_to_ms(t["due_date"]),
            "priority": t["priority"]
        }
        
        try:
            # Create Parent Task
            task_url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
            created_task = clickup_api_request(task_url, "POST", headers, task_payload)
            task_id = created_task.get("id")
            print(f"    -> Created Parent Task (ID: {task_id})")
            
            # Update Points if Custom Field matches and points > 0
            if points_field_id and t["points"] > 0:
                print(f"    -> Setting points to {t['points']}...")
                cf_url = f"https://api.clickup.com/api/v2/task/{task_id}/field/{points_field_id}"
                clickup_api_request(cf_url, "POST", headers, {"value": t["points"]})
                
            # Create Nested Subtasks (omitted 'status' to let ClickUp default to list open status)
            for st_name in t["subtasks"]:
                st_payload = {
                    "name": st_name,
                    "parent": task_id
                }
                clickup_api_request(task_url, "POST", headers, st_payload)
                print(f"       + Created subtask: '{st_name}'")
                
            print("    -> Done!\n")
            
        except Exception as e:
            print(f"\n[ERROR] Failed to import task '{t['name']}' due to an error. Aborting execution to prevent a partially imported state.")
            sys.exit(1)
            
    print("\n====================================================")
    print("       SUCCESS! All ClickUp tasks are imported!      ")
    print("====================================================")

if __name__ == "__main__":
    main()
