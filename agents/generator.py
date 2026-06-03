import os 
from anthropic import Anthropic
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate(cv_path, company_name, job_title, job_description, candidate_name, notes=None):
    if cv_path.endswith(".pdf"):
        import fitz
        doc = fitz.open(cv_path)
        cv_content = ""
        for page in doc:
            cv_content += page.get_text()
    else:
        cv_content = Path(cv_path).read_text(encoding="utf-8")

    cover_letter_template = (PROMPTS_DIR/"cover_letter.txt").read_text(encoding="utf-8")
    email_template = (PROMPTS_DIR/"email_draft.txt").read_text(encoding="utf-8")
    study_guide_template = (PROMPTS_DIR/"study_guide.txt").read_text(encoding="utf-8")

    cover_letter_prompt = cover_letter_template.format(
        cv_content = cv_content,
        company_name = company_name,
        job_title = job_title,
        job_description = job_description
    )

    if notes:
        cover_letter_prompt += f"\n\nUser feedback on previous attempt : {notes}"


    email_prompt = email_template.format(
        candidate_name = candidate_name,
        company_name = company_name,
        job_title = job_title
    )

    study_guide_prompt = study_guide_template.format(
        cv_content=cv_content,
        company_name=company_name,
        job_title=job_title,
        job_description=job_description
    )

    cover_letter_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {"role":"user","content": cover_letter_prompt}
        ]
    )

    email_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[
            {"role":"user","content": email_prompt}
        ]
    )

    study_guide_response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=3000,
    messages=[
        {"role": "user", "content": study_guide_prompt}
    ]
    )

    cover_letter = cover_letter_response.content[0].text
    email_draft = email_response.content[0].text
    study_guide = study_guide_response.content[0].text

    return cover_letter, email_draft, study_guide