# Job Application Assistant

A CLI tool that helps you apply for jobs faster. You paste a job description, it generates a tailored cover letter, email draft, and interview study guide using the Claude API. You review everything in the terminal before anything is saved or sent.

## How It Works

```
You input job details
       |
       v
Claude generates cover letter + email draft + study guide
       |
       v
You review in terminal — approve / edit / reject
       |
       v (approved)
Saves .docx and .pdf locally
Logs to Google Sheets
Creates Gmail draft (optional)
```

If you choose **edit**, you type what to change (e.g. "make it shorter", "more formal tone") and Claude regenerates with your feedback. You can edit as many times as you want before approving.

## Features

- Tailored cover letter generated from your CV and the job description
- Email draft ready to send
- Interview study guide with likely questions and talking points
- Human-in-the-loop review loop with iterative feedback
- Saves output as `.docx` and `.pdf`
- Logs each application to Google Sheets
- Creates Gmail draft with PDF attached

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Anthropic SDK | Claude Haiku for all generation |
| PyMuPDF | Reads CV from PDF |
| python-docx + fpdf2 | Outputs cover letter as .docx and .pdf |
| gspread | Logs applications to Google Sheets |
| Google API client | Creates Gmail drafts via OAuth2 |
| python-dotenv | Loads secrets from .env |
| PyYAML | Reads config.yaml |

## Setup

**1. Clone and install dependencies**

```bash
git clone https://github.com/haniszaim/Job-Application-Assistant-.git
cd Job-Application-Assistant-
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**2. Create a `.env` file**

```
ANTHROPIC_API_KEY=your_key_here
SHEET_ID=your_google_sheet_id_here
```

**3. Add your credentials**

```
credentials/
    google_credentials.json   # Service account key for Google Sheets
    gmail_credentials.json    # OAuth2 client credentials for Gmail
```

**4. Add your CV**

```
cv/
    YOUR_RESUME.pdf
```

**5. Update `config.yaml`**

```yaml
candidate_name: "Your Name"
cv_path: "cv/YOUR_RESUME.pdf"
sheet_name: "Job Applications 2026"
```

## Usage

```bash
python main.py
```

You will be prompted to enter:

```
Company > Grab
Role > AI Engineer
Job URL > https://...
Location > Kuala Lumpur
Paste job description > ...
```

Then Claude generates everything and shows it in the terminal. You choose:

```
[a] Approve   [e] Edit   [r] Reject
```

If you edit, type your feedback and Claude regenerates immediately.

## Output

Each approved application creates a folder under `output/`:

```
output/
    Grab_AI_Engineer_2026-06-03/
        cover_letter.docx
        cover_letter.pdf
        study_guide.md
```

And logs a row to your Google Sheets tracker with date, company, role, URL, location, file path, and status.

## Project Structure

```
job-apply-bot/
    main.py                  # Entry point and pipeline orchestration
    config.yaml              # Candidate config
    agents/
        generator.py         # Claude API calls
        approval.py          # Terminal review UI
        file_saver.py        # Saves .docx and .pdf
        tracker.py           # Google Sheets logging
        gmail.py             # Gmail draft creation
    prompts/
        cover_letter.txt     # Prompt template
        email_draft.txt      # Prompt template
        study_guide.txt      # Prompt template
```
