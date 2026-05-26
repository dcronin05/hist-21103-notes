# ClickUp Integration & Sync Guide for Coding Agents

This document is a comprehensive, self-contained developer guide for programming assistants. It compiles all API endpoints, payload shapes, standard library implementations, link-rewriting logic, and formatting constraints needed to programmatically synchronize course syllabi, assignments, subtasks, media attachments, and documents directly into ClickUp.

---

## 1. Credentials & List Metadata Extraction
ClickUp API v2 requires a Personal API Token. All requests must include:
*   Header: `"Authorization": "YOUR_API_TOKEN"`
*   Header: `"Content-Type": "application/json"` (except when uploading files)

### Workspace ID Retrieval
The Workspace ID (`team_id`) is required for Docs v3 API endpoints but is **not** returned by the List Details endpoint (`GET /api/v2/list/{list_id}`). It must be recovered by querying the user's teams:
*   **Endpoint**: `GET https://api.clickup.com/api/v2/team`
*   **Extraction**: Access the first workspace ID: `data["teams"][0]["id"]`.

### Custom Field (Points) Query
To map course grades/points to a custom ClickUp number field, query the list's active fields:
*   **Endpoint**: `GET https://api.clickup.com/api/v2/list/{list_id}/field`
*   **Identification**: Loop through fields and locate `field["name"].lower() == "points"`. Save `field["id"]` to update tasks.

---

## 2. ClickUp Tasks & Subtasks
### Creation & In-Place Updates
*   **Create Task**: `POST https://api.clickup.com/api/v2/list/{list_id}/task`
*   **Update Task**: `PUT https://api.clickup.com/api/v2/task/{task_id}`
*   **Payload Shape**:
    ```json
    {
      "name": "Task Name",
      "markdown_content": "# Rich Text Description\n- [ ] Checklist Item",
      "start_date": 1779740400000,
      "due_date": 1779913200000,
      "priority": 3
    }
    ```

### Crucial API Constraints & Best Practices:
1.  **Omit Status**: Do not hardcode `"status": "to do"` or `"status": "open"` in creation payloads. Doing so causes `400 Bad Request` if the space uses a custom open status (e.g. `"not started"`). Leave the status field out, and ClickUp will automatically assign the list's default open status.
2.  **Priority Value Mapping**: Priorities are strictly represented by integers:
    *   `1` = Urgent
    *   `2` = High
    *   `3` = Normal
    *   `4` = Low
3.  **Custom Field Updates**: To set custom fields like "Points", you must send a separate `POST` request:
    *   **Endpoint**: `POST https://api.clickup.com/api/v2/task/{task_id}/field/{custom_field_id}`
    *   **Body**: `{"value": 50}` (must match field type, i.e., numeric value for number fields).
4.  **Local-centric Timestamps**: Convert `MM/DD/YYYY` dates to POSIX milliseconds. To prevent local-to-UTC offsets from rolling dates back to the previous calendar day, replace the hour with a safe buffer (e.g., `8:00 AM` local time) before generating the timestamp:
    ```python
    dt = datetime.datetime.strptime(date_str, "%m/%d/%Y").replace(hour=8, minute=0, second=0)
    millis = int(dt.timestamp() * 1000)
    ```

### Subtasks Linkage
*   To link a subtask to a parent task, include the `"parent": parent_task_id` attribute inside the standard Create Task body.
*   **In-Place Matching**: To update subtasks without wiping activity history, match local names to ClickUp subtasks. Query task list with `?subtasks=true` to load parent-subtask relations, matching subtask titles case-insensitively.

---

## 3. Dynamic Subtask Scheduling
To populate Gantt/Timeline views, subtasks should be scheduled sequentially within the parent task's duration based on keyword-defined "study phases":

```python
def classify_subtask(name):
    n = name.lower()
    if any(k in n for k in ["submit", "upload", "turn in"]): return 3  # Submission
    if any(k in n for k in ["draft", "write", "compare", "analyze", "setup"]): return 2  # Drafting
    return 1  # Reading & Research (Default)
```

### Date Calculations (given parent duration $D$):
*   **Phase 1 (Reading & Research)**: Start at parent `start_date`. Span up to 50% of parent duration.
*   **Phase 2 (Drafting & Writing)**: Start at 40% of parent duration. Due 1 day before parent `due_date` (or *on* parent `due_date` if no Phase 3 subtask exists).
*   **Phase 3 (Submission)**: Start 1 day before parent `due_date`. Due on parent `due_date`.

---

## 4. Task-Bound Documents (ClickUp Docs v3 API)
Instead of placing notes at the root of a workspace, attach them as "Task-bound Documents" directly inside parent tasks/subtasks.

*   **Create Doc**: `POST https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs`
*   **Payload**:
    ```json
    {
      "name": "Document Name",
      "parent": {
        "id": "CLICKUP_TASK_ID",
        "type": 1
      },
      "create_page": true
    }
    ```
    *   *Type `1` specifies task parenting (as opposed to workspace-level docs).*
*   **Query Existing Docs**: `GET https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs` (collects `doc_id` and name to match in-place).
*   **Update Page Content**:
    *   **Endpoint**: `PUT https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}`
    *   **Body**:
        ```json
        {
          "name": "Page Name",
          "content": "# Clean Markdown Content",
          "content_format": "text/md"
        }
        ```
    *   Note: To retrieve the `{page_id}` of the default page created during Doc instantiation, run a `GET` on `https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}/pages`.

### API Deletion Limitation
The ClickUp REST API returns a `405 Method Not Allowed` for `DELETE` calls on Documents. **Programmatic document deletion is disabled**. Old/cluttered workspace documents must be manually deleted or archived by the user in the ClickUp UI.

---

## 5. Media Asset Uploads (Attachment API)
ClickUp allows uploading non-markdown media assets (images, PDFs, audio) directly to tasks.
*   **Endpoint**: `POST https://api.clickup.com/api/v2/task/{task_id}/attachment`
*   **Format**: Multipart Form-Data (Multipart/form-data)

Here is a pure Python implementation using `urllib` to avoid third-party libraries (like `requests`):

```python
import urllib.request
import urllib.error
import mimetypes
import uuid
import os
import json

def upload_attachment(task_id, file_path, headers):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/attachment"
    boundary = f"Boundary-{uuid.uuid4().hex}"
    
    with open(file_path, "rb") as f:
        file_content = f.read()
        
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    
    # Construct multipart request payload
    part_header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="attachment"; filename="{filename}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8")
    part_footer = f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    req_body = part_header + file_content + part_footer
    
    req = urllib.request.Request(url, data=req_body, method="POST")
    req.add_header("Authorization", headers["Authorization"])
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Content-Length", str(len(req_body)))
    
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Upload failed: {e.read().decode('utf-8')}")
        return None
```

---

## 6. Markdown Cleaning & Callout Conversion
ClickUp's markdown renderer does not support YAML frontmatter blocks or GitHub-style colorful callout banners. Standardize pages by stripping or formatting these blocks before sending payloads to ClickUp:

### YAML Frontmatter Stripper
Removes the `---` blocks from the top of markdown documents:
```python
def strip_frontmatter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip()
    return content
```

### Callout Transformation
ClickUp renders standard blockquotes (`>`) perfectly, but displays syntax like `> [!IMPORTANT]` literally. Translate these into standard blockquotes using descriptive bold headers and unicode emojis:
```python
import re

CALLOUT_RE = re.compile(r'^>\s*\[!(NOTE|IMPORTANT|TIP|CAUTION|WARNING)\]', re.IGNORECASE | re.MULTILINE)

def clean_callouts(content):
    def replace_callout(match):
        c_type = match.group(1).upper()
        if c_type == "NOTE": return "> ℹ️ **NOTE:**"
        if c_type == "IMPORTANT": return "> ⚠️ **IMPORTANT:**"
        if c_type == "TIP": return "> 💡 **TIP:**"
        if c_type == "CAUTION": return "> ⚠️ **CAUTION:**"
        if c_type == "WARNING": return "> 🛑 **WARNING:**"
        return f"> **{c_type}:**"
    return CALLOUT_RE.sub(replace_callout, content)
```

---

## 7. Dynamic Relative Link Rewriting
When notes reference local relative markdown files (e.g. `../readings/chapter_01.md`), ClickUp descriptions and Document pages will break. You must intercept and rewrite these links:

1.  **Map Target IDs**: During Pass 1 (Task/Subtask sync) and Pass 2 (Doc creation), capture mappings of:
    *   `doc_map`: `local_file_path` $\rightarrow$ `https://app.clickup.com/{workspace_id}/v/dc/{doc_id}`
    *   `asset_map`: `local_asset_path` $\rightarrow$ `https://t9006041408.p.clickup-attachments.com/...`
2.  **Relative Link Resolver**: For each link `[Label](url)` parsed in the file:
    *   Ignore absolute URLs (`http://`, `https://`).
    *   Strip fragments/anchors (`#heading`) temporarily to match the file path, but save them.
    *   Calculate the relative path target starting from the current file's directory:
        ```python
        joined = os.path.join(os.path.dirname(current_file), url)
        canonical = os.path.normpath(joined).replace("\\", "/")
        ```
    *   Look up `canonical` in the `doc_map` or `asset_map`.
    *   Replace the relative link with the resolved ClickUp URL, appending any saved fragment anchors (e.g. `[Label](https://app.clickup.com/123/v/dc/abc#heading-anchor)`).
