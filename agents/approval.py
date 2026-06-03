from pathlib import Path

def review(company, job_title, cover_letter, email_draft, study_guide):
    print("\n" + "="*60)
    print(f"COMPANY : {company}")
    print(f"ROLE    : {job_title}")
    print("="*60)
    print("\n--- COVER LETTER ---\n")
    print(cover_letter)
    print("\n--- EMAIL DRAFT ---\n")
    print(email_draft)
    print("\n" + "="*60)
    print("\n--- STUDY GUIDE ---\n")
    print(study_guide)

    while True:
        choice = input("\n[a] Approve [e] Edit [r] Reject > ").strip().lower()
        if choice =="a":
            return "approved"
        elif choice == "e":
            note = input("what to change? > ")
            return ("edit", note)
        elif choice == "r":
            return "rejected"
        else:
            print("invalid Input. Type a , e or r.")
    