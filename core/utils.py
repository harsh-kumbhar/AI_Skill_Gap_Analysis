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

import pandas as pd
import ast

def get_ai_recommendations(dream_role_name, user_skills, dataset_path="core/data/job_roles.csv"):
    """
    Returns data-driven AI-like recommendations based on job-skill dataset.
    """
    try:
        df = pd.read_csv(dataset_path)

        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]

        # Find matching rows for dream role
        matched = df[df["job_title"].str.lower().str.contains(dream_role_name.lower(), na=False)]

        if matched.empty:
            return ["No AI recommendations available for this dream role yet."]

        # Collect all skills for that role
        all_role_skills = set()
        for row in matched["job_skill_set"]:
            try:
                # Convert string list to Python list
                skills_list = ast.literal_eval(row)
                all_role_skills.update([s.strip() for s in skills_list])
            except:
                continue

        # Filter missing ones
        missing = [s for s in all_role_skills if s not in user_skills]

        # Create readable recommendations
        recommendations = []
        for skill in missing:
            recommendations.append(f"Learn or improve your skill in **{skill}**, commonly required for {dream_role_name} roles.")

        if not recommendations:
            recommendations.append("Great job! You already have most of the skills needed for this role.")

        return recommendations

    except Exception as e:
        print(f"Error in AI recommendation: {e}")
        return ["⚠️ Error generating recommendations."]
