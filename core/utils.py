# core/utils.py
import re
from PyPDF2 import PdfReader
from .models import Skill

def extract_skills_from_resume(pdf_file):
    """
    Extracts text from the uploaded resume PDF and detects known skills.
    Returns a list of matched skill names.
    """
    text = ""

    try:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []

    # Normalize text for case-insensitive matching
    text = text.lower()

    # Get all known skills from DB
    all_skills = Skill.objects.values_list("name", flat=True)
    detected_skills = []

    for skill in all_skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            detected_skills.append(skill)

    return list(set(detected_skills))
