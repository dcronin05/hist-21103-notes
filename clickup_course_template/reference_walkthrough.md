# Walkthrough - Wiki Organization Nesting & Assignment Score Tracker Redesign

We have successfully refactored the course Wiki outline into a nested, content-bearing parent structure, and redesigned the client-side HTML dashboard into a gorgeous local **Assignment Score & Feedback Tracker**.

## Changes Made

### 1. Assignment Score & Feedback Tracker Dashboard
We overhauled [clickup_tasks_dashboard.html](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/notes/clickup_tasks_dashboard.html) from a copy-paste setup hub into an outcome tracking site:

* **Dynamic Statistics Panel**:
  * **Current Course Grade**: An interactive SVG circular gauge showing your current overall percentage and letter grade (A, B, C, D, F) dynamically computed based on earned points.
  * **Points Accumulated**: A running tracker of earned points out of the course total (450 max points possible).
  * **Submissions Logged**: Real-time counter of how many assignments have been marked as turned in (`X / 13`).
  * **Graded Performance**: Computes average score percentage dynamically across only the tasks that have received numerical grades.
* **Progress Threshold Bar**: Displays your visual path towards maximum points (450) with indicator points mapped for D (270 pts), C (315 pts), B (360 pts), and A (405 pts) grade boundaries.
* **Outcome Entry Panel (on cards)**:
  * **Three-Way Status Toggle Button**: A custom-styled linear toggle button that cycles between three states: `Not Submitted` (gray), `Submitted` (orange/pending grade), and `Graded` (green). Clicking it loops through these states.
  * **Score Input (Dropdown)**: An elegant dropdown select picker from `0` to `max points` (in steps of `0.5` points) that dynamically appears/slides open *only* when the status is toggled to `Graded`. Selecting a score dynamically calculates the course grade.
  * **Feedback Log**: A dedicated text area to save deductions, corrections, or grading comments from the professor.
  * **Dynamic Status Indicators**: Tasks visually update their border glow and badges depending on state: `NOT SUBMITTED` (default), `PENDING GRADE` (orange glow/pulse), or `GRADED` (green glow).
* **State Persistence**: All scores, submission statuses, and feedback logs are saved in the browser's `localStorage` (automatically loaded on page refresh). A red **"Reset All Inputs"** button is provided to clear all tracker data.
* **Gantt Schedule Integration**: The Gantt chart bars dynamically update their colors based on submission status: green if graded (showing received score), amber/orange if pending grade, or default theme if not submitted.

---

### 2. Nested Wiki Structure
We restructured the central Wiki Outline in [import_to_clickup.py](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/notes/import_to_clickup.py) to nest all child prompts and readings under content-rich parent pages (entirely eliminating empty heading categories):

* **Syllabus & Guides**: Nested under **Course Syllabus** parent page.
* **1619 Book Structure**: 
  * Front and back book matter (Preface, Copyright, Dedication, Authors Note, Index, References) nested under the **1619 Book Overview** page.
  * Chapters nested under the corresponding assignment's **Lecture Notes** parent page (e.g., `1619 Introduction` and `Chapter 1` nested under `Colonial Settlement Lecture Notes`).
* **Groupings**: Prompts and readings are nested under their respective **Lecture Notes** pages, grouping all resources for each week's milestone under a single content-rich parent.
* **Link Rewriting**: Successfully traversed the hierarchy and rewrote all links in task/subtask descriptions and document content to point directly to the new nested ClickUp Wiki page locations (`/p/{page_id}`).

---

## Verification Results

1. **Dashboard UI Checks**:
   - Toggling "Submitted" updates status badges and increases the submission count.
   - Inputting a score dynamically updates accumulated points, percentage, letter grade gauge, and overall progress bar.
   - Refreshed browser tab and verified that all states (grades, switches, feedback logs) persisted from `localStorage`.
   - Out-of-bounds inputs (e.g. typing `60` for a `50`-point task) are automatically normalized back to the maximum allowed limit.
2. **Git Sync**:
   - Executed final push to remote origin. The repository is up-to-date and clean.

## Output Files
* **Tracker Dashboard**: [clickup_tasks_dashboard.html](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/notes/clickup_tasks_dashboard.html)
* **Sync Script**: [import_to_clickup.py](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/notes/import_to_clickup.py)
