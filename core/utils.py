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
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.cluster import KMeans
import numpy as np

# --- Model Initialization ---
# This is loaded once and reused, making the function efficient.
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_ai_recommendations(dream_role_name, user_skills, dataset_path="core/data/job_roles.csv"):
    """
    Generates a detailed skill analysis report using semantic clustering to identify strengths and growth areas.
    """
    try:
        df = pd.read_csv(dataset_path)
        df.columns = [c.strip().lower() for c in df.columns]

        # --- 1. Find the Dream Role and Extract Required Skills ---
        matched = df[df["job_title"].str.lower().str.contains(dream_role_name.lower(), na=False)]
        if matched.empty:
            return [f"No AI recommendations available for '{dream_role_name}' yet. The role might not be in our dataset."]

        all_role_skills = set()
        for row in matched["job_skill_set"]:
            try:
                skills_list = ast.literal_eval(row)
                all_role_skills.update([s.strip().title() for s in skills_list])
            except (ValueError, SyntaxError):
                continue

        # --- 2. Skill Preprocessing ---
        role_skills_clean = sorted([s for s in all_role_skills if s.lower() not in ENGLISH_STOP_WORDS and len(s) > 1])
        user_skills_clean = sorted(list(set(user_skills)))

        if not role_skills_clean:
            return ["Could not extract a clear list of skills for this role."]

        # --- 3. Semantic Analysis: Strengths and Gaps ---
        role_embeddings = model.encode(role_skills_clean, convert_to_tensor=True)
        user_embeddings = model.encode(user_skills_clean, convert_to_tensor=True)
        similarity_matrix = util.cos_sim(user_embeddings, role_embeddings)

        # Identify user's strengths (skills that are highly relevant)
        user_strengths = []
        for i, user_skill in enumerate(user_skills_clean):
            if float(similarity_matrix[i].max()) > 0.65: # Higher threshold for a confirmed strength
                user_strengths.append(user_skill)

        # Identify missing skills (gaps)
        role_similarity_scores = util.cos_sim(role_embeddings, user_embeddings)
        missing_skills = []
        for i, skill in enumerate(role_skills_clean):
            if float(role_similarity_scores[i].max()) < 0.55: # Threshold for a skill gap
                missing_skills.append(skill)
        
        # --- 4. Generate a Structured Report ---
        report = []
        report.append(f"### 💡 AI Skill Analysis for a aspiring '{dream_role_name}'")
        
        # Add Strengths Section
        if user_strengths:
            report.append("\n---")
            report.append("### ✅ Your Strengths")
            report.append("Great job! These skills from your profile are highly relevant and form a strong foundation:")
            report.append(f"**Key Assets:** *{', '.join(user_strengths[:8])}*")
        
        if not missing_skills:
            report.append("\n---")
            report.append("### 🎉 Excellent Alignment!")
            report.append("Your skills are already very well-aligned with the requirements for this role. Keep refining your projects and experience!")
            return report

        # --- 5. Advanced NLP: Cluster Missing Skills into Growth Areas ---
        report.append("\n---")
        report.append("### 🌱 Your Growth Areas")
        report.append("To become a top candidate, focus on developing skills in these thematic areas:")
        
        if len(missing_skills) < 5: # If very few skills, just list them
            report.append(f"• **Next Steps:** Consider learning *{', '.join(missing_skills)}* to round out your profile.")
        else:
            # Cluster the missing skills based on their meaning
            missing_embeddings = model.encode(missing_skills)
            num_clusters = max(2, min(5, len(missing_skills) // 3)) # Dynamic number of clusters
            clustering_model = KMeans(n_clusters=num_clusters, n_init='auto', random_state=42)
            clustering_model.fit(missing_embeddings)
            clusters = [[] for _ in range(num_clusters)]
            for i, skill in enumerate(missing_skills):
                clusters[clustering_model.labels_[i]].append(skill)
            
            # Create a recommendation for each cluster
            for i, cluster in enumerate(clusters):
                if not cluster: continue
                # Find a representative name for the cluster (e.g., the most common starting word or just a generic title)
                cluster_title = f"Area #{i+1}: Mastering {cluster[0].split(' ')[0]}"
                report.append(f"\n• **{cluster_title}**")
                report.append(f"  *Sharpen your expertise in:* {', '.join(sorted(cluster))}")
            
        # Clean Markdown symbols before sending to frontend
        cleaned_report = [re.sub(r"[#*_`]", "", line).strip() for line in report]
        return cleaned_report

    except FileNotFoundError:
        return [f"⚠️ Error: The dataset file was not found at the path '{dataset_path}'."]
    except Exception as e:
        print(f"An unexpected error occurred in AI recommendation: {e}")
        return ["⚠️ An unexpected error occurred while generating recommendations."]

def recommend_courses(missing_skills):
    df = pd.read_csv("core/data/course_data.csv")
    recommendations = []

    for skill in missing_skills:
        matches = df[df['skill'].str.lower() == skill.lower()]
        for _, row in matches.iterrows():
            recommendations.append({
                'skill': skill,
                'course_name': row['course_name'],
                'platform': row['platform'],
                'url': row['url'],
                'description': row['description']
            })
    return recommendations