from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Skill database
SKILLS_DB = ["Python", "Machine Learning", "Deep Learning", "SQL", "Data Science", "React", "AWS", "NLP"]

def extract_skills(text):
    return [skill for skill in SKILLS_DB if skill.lower() in text.lower()]

def compute_similarity(resume_text, job_desc):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_desc])
    return cosine_similarity(vectors)[0, 1]
