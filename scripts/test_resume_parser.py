from app.services.resume_parser import extract_resume_text

resume_text = extract_resume_text(r"C:\Users\DELL\OneDrive\Desktop\Aniket_Resume.pdf")
print("Extracted Resume Text:")
print(resume_text[:3000])