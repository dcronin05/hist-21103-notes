# Transform ClickUp Planner into Assignment Score & Feedback Tracker

We will transform the client-side HTML dashboard [clickup_tasks_dashboard.html](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/notes/clickup_tasks_dashboard.html) into an **Assignment Score & Feedback Tracker**.

## User Review Required

We propose to replace the "ClickUp Sync" and "Copy Hub" functionality with direct assignment performance tracking. All historical course data, due dates, and descriptions will be preserved, but the interactive components will change.

## Proposed Changes

### 1. Header & Metadata Redesign
* Rename title to **HIST 21103 — Assignment Score & Feedback Tracker**.
* Update description to focus on grade accumulation, submission tracking, and instructor feedback logs.

### 2. Header Score Widget (Dynamic Calculator)
Replace the simple progress bar with a comprehensive grade dashboard:
* **GPA / Letter Grade Indicator**: Displays current grade letter (A, B, C, D, F) based on total accumulated points.
* **Earned Points Tracker**: Displays `Earned Points / Total Possible Points (450)`.
* **Submission Counter**: Displays how many of the 13 assignments have been marked as "Submitted".
* **Interactive Progress Bar**: Visualizes progress toward maximum points (450).

### 3. Interactive Assignment Cards
Inside each assignment card, we will replace the copy blocks with a dedicated **Performance Entry Panel**:
* **Submission Toggle**: A custom styled switch/checkbox for marking the assignment as "Submitted".
* **Score Input**: A styled numeric input field `[ __ ] / Max Points` with validation checking (0 to max points). For 0-point assignments, it will show a "Mark Complete" toggle instead.
* **Feedback Log**: A multi-line textarea for logging the professor's comments and corrections.
* **Dynamic Status Badges**:
  * `NOT SUBMITTED` (Gray / Red border)
  * `SUBMITTED (PENDING GRADE)` (Orange / Warning border)
  * `GRADED` (Green / Success border)

### 4. Local Storage Persistence
* Save scores, submission states, and feedback values to `localStorage` keyed by assignment ID.
* Automatically load and recalculate stats on page load.
* Create a **"Reset All Data"** button to clear entries if needed.

### 5. Unified Layout Cleanups
* Retain the **Gantt Chart timeline** for visual schedule reference.
* Remove the CSV download buttons, setup guides, and tabs, as the focus is now entirely on score tracking.
* Retain assignment description and requirements summaries for easy reference while writing.

---

## Verification Plan

### Manual Verification
* Open the modified [clickup_tasks_dashboard.html](file:///Users/dcronin05/Library/CloudStorage/OneDrive-SharedLibraries-dcron.in/School%20-%20Documents/Classes/HIST%2021103/notes/notes/clickup_tasks_dashboard.html) in a web browser.
* Toggle an assignment as submitted and verify that the status badge updates to `PENDING GRADE` and the submission count increases.
* Input a score (e.g. `45` out of `50`) and verify that the accumulated points, grade percentage, letter grade, and progress bar dynamically update in real time.
* Enter sample feedback text, refresh the browser page, and verify that all inputs, scores, and status states persist.
* Test score inputs outside limits (e.g. negative values or greater than max points) to verify boundaries.
