# Guide for Recreating Class Wiki & Grade Tracker in ClickUp

This directory contains template and reference files to recreate a unified **ClickUp Course Wiki, Assignment Planner, and Local Grade Tracker** for a different class.

---

## 1. System Architecture Overview

The system consists of two major components working together:

### A. Python ClickUp Syncer (`reference_import_to_clickup.py`)
This script uses standard Python libraries (`urllib` and `re`) to sync local markdown course files and checklist tasks directly to the ClickUp API. It executes in three distinct passes to solve relational dependencies:

1. **Pass 1 (Tasks & Subtasks Sync)**:
   * Connects to your ClickUp List.
   * Creates or matches in-place the parent tasks (e.g. Essays, Orientation) with start dates, due dates, priority tags, and points.
   * Calculates subtask dates (distributing them dynamically across the parent's timeline based on *Study Phase* keywords like "read", "draft", "submit").
   * Creates/updates subtasks under each parent, saving all task and subtask ClickUp IDs.
2. **Pass 2 & 2.9 (Wiki & Document Sync)**:
   * Locates or creates a central **Wiki Document** (`type: 2`) in the ClickUp workspace.
   * Traverses a nested page tree defined in `wiki_structure`. It recursively creates nested subpages (using `parent_page_id`) and maps them to local file paths.
   * Sanitizes local markdown contents (stripping frontmatter, transforming GitHub-style alert callouts into ClickUp blockquotes with emojis).
   * Updates Wiki page contents on ClickUp and maps every local file to its specific ClickUp Wiki subpage URL (`/p/{page_id}`).
3. **Pass 3 (Description & Link Sync)**:
   * Scans all task/subtask descriptions and Wiki pages for relative markdown file paths (e.g. `../readings/file.md`).
   * Canonicalizes and rewrites these paths into active ClickUp Wiki subpage URLs (`/p/{page_id}`).
   * Updates all task/subtask descriptions in-place on ClickUp and adds automated comments to notify you that descriptions have been synced.

### B. Local Grade & Feedback Tracker (`reference_clickup_tasks_dashboard.html`)
This is a self-contained local HTML dashboard that serves as a student grade log.
* **Grade Gauge**: Displays overall percentage, progress bar towards letter thresholds (A, B, C, D, F), and total accumulated points.
* **Assignment Cards**: Contains checklists, due dates, description files, and custom inputs:
  * A **Three-Way Cycle Button**: Linearly toggles the status of each assignment (`Not Submitted` ➡️ `Submitted` ➡️ `Graded`).
  * A **Grade select picker**: Dropdown select options from `0` to the task's maximum points in steps of `0.5` points (displays *only* when the state is toggled to `Graded`).
  * A **Feedback Textarea**: Text area for recording professor feedback.
* **State Persistence**: Saves all scores, statuses, and feedback directly to `localStorage` (automatically load/recalculate on refresh).
* **Gantt Schedule**: An interactive visual Gantt timeline that dynamically updates its bar colors based on submission status.

---

## 2. Adaptation Checklist for a New Course

To adapt this setup for a new class, a future agent should follow these steps:

### Step 1: Prepare the Course Markdown Corpus
1. Group course materials into a structured directory (e.g., `syllabus.md`, `readings/`, `assignments/`, `lectures/`).
2. Write individual markdown pages for course materials.
3. Link pages together using standard relative paths (e.g. `[Hamdani Reading](../readings/hamdani.md)`). The syncer will automatically rewrite these into ClickUp Wiki links during execution.

### Step 2: Configure the ClickUp Importer Script
Modify the following sections in `reference_import_to_clickup.py`:
1. **`tasks_data`** (Line ~10): Define your course assignments, checklists, start/due dates, priority values, and max points.
2. **`markdown_files`** (Line ~243): Map local file paths to their friendly document names.
3. **`get_doc_title`** (Line ~284): Add the page title strings for all your markdown files.
4. **`wiki_structure`** (Line ~669): Define the nested layout tree. Use `None` for top-level pages, or parent file paths (e.g. `"notes/syllabus.md"`) to nest children.
5. **Credentials**: Update `default_token` (Line ~1066) and `default_list_id` (Line ~1067).

### Step 3: Configure the Local Grade Tracker
Modify the following sections in `reference_clickup_tasks_dashboard.html`:
1. **`courseData`** (Line ~730): Update this Javascript array with your new milestones, dates, tasks, point allocations, descriptions, and subtasks. Ensure task `id`s are unique integers.
2. **Calculations**: Update `totalMaxPoints` (Line ~1365) and thresholds inside `getGradeScaleMsg` (Line ~1350) to match the new course grading scale.
3. **Local Storage Key**: Customize the `localStorage` key (Line ~1189) to prevent data overlapping with other courses (e.g. `hist_21103_grade_tracker` &rarr; `math_101_grade_tracker`).

### Step 4: Run & Sync
1. Run the Python syncer to generate the ClickUp Wiki and sync task descriptions:
   ```bash
   python3 import_to_clickup.py --non-interactive
   ```
2. Open the customized `clickup_tasks_dashboard.html` in your browser to begin tracking grades.

---

## 3. Reference Files List

Use these files in this directory to understand the historical setup:
* [reference_implementation_plan.md](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/clickup_course_template/reference_implementation_plan.md) - The original approved implementation plan.
* [reference_walkthrough.md](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/clickup_course_template/reference_walkthrough.md) - The walkthrough summarizing performance and date scheduling.
* [reference_task.md](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/clickup_course_template/reference_task.md) - The checklist showing completed tasks.
* [reference_import_to_clickup.py](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/clickup_course_template/reference_import_to_clickup.py) - The finalized pure-Python ClickUp syncer code.
* [reference_clickup_tasks_dashboard.html](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/clickup_course_template/reference_clickup_tasks_dashboard.html) - The dynamic Assignment Score and Feedback Tracker HTML dashboard.
