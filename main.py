import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
from agents.generator import generate
from agents.tracker import log_application
from agents.approval import review
from agents.file_saver import save_files
from agents.gmail import create_draft


load_dotenv()

BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)


def run_pipeline(company, role, url, location, job_description, source="Manual"):
    print(f"\nProcessing: {company} - {role}")

    notes = None
    while True:
        cover_letter, email_draft, study_guide = generate(
            cv_path=config["cv_path"],
            company_name=company,
            job_title=role,
            job_description=job_description,
            candidate_name=config["candidate_name"],
            notes=notes
        )

        result = review(company, role, cover_letter, email_draft, study_guide)

        if result == "approved":
            docx_path, pdf_path, study_guide_path = save_files(
                company=company,
                role=role,
                cover_letter=cover_letter,
                study_guide=study_guide
            )
            log_application(
                company=company,
                role=role,
                url=url,
                source=source,
                location=location,
                cover_letter_path=pdf_path,
                cv_version=Path(config["cv_path"]).name,
                status="To Apply"
            )
            print("Files saved")
            print("Logged to Google Sheets")

            if source == "Manual":
                to_email = input("Recipient email address (Enter to skip) > ").strip()
                if to_email:
                    subject = f"Application for {role} - {company}"
                    create_draft(
                        to_email=to_email,
                        subject=subject,
                        email_body=email_draft,
                        pdf_path=pdf_path
                    )
                    print("Gmail draft created")
            break

        elif isinstance(result, tuple) and result[0] == "edit":
            notes = result[1]
            print(f"Edit note: {notes}")
            print("Re-running generator with your note..")

        elif result == "rejected":
            print("Skipped.")
            break


if __name__ == "__main__":
    run_pipeline(
        company=input("Company > "),
        role=input("Role > "),
        url=input("Job URL > "),
        location=input("Location > "),
        job_description=input("Paste job description > "),
        source="Manual"
    )