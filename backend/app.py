from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sqlite3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.file_processing import extract_text_from_pdf, extract_text_from_docx
from utils.text_processing import preprocess_text
from utils.matching import extract_skills, compute_similarity
from models.model_training import predict_resume_score
import os
import tempfile

app = Flask(__name__)

# ✅ Correctly configure CORS with credentials
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['CORS_ORIGINS'] = ['http://localhost:3000']
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_resume_embedding(text):
    return model.encode(text).astype(np.float32)

# Database setup
conn = sqlite3.connect("resumes.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        skills TEXT,
        similarity_score REAL,
        ats_score REAL
    )
""")
conn.commit()

# FAISS setup
dimension = 384
index = faiss.IndexFlatL2(dimension)
try:
    index = faiss.read_index("faiss_index.idx")
except:
    pass

@app.route("/api/upload", methods=["POST"])
@cross_origin(origins='http://localhost:3000', supports_credentials=True)
def upload_resume():
    resume_file = request.files["resume"]
    job_desc = request.form["job_desc"]

    # Save resume temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.filename)[-1]) as tmp:
        resume_file.save(tmp.name)
        temp_path = tmp.name  # Save path for later use

    # Extract text after file is closed
    if resume_file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(temp_path)
    else:
        resume_text = extract_text_from_docx(temp_path)

    # Delete temp file now
    try:
        os.remove(temp_path)
    except Exception as e:
        print(f"Warning: Could not delete temp file {temp_path}: {e}")

    # Process resume and compute scores
    processed_resume = preprocess_text(resume_text)
    skills = extract_skills(processed_resume)
    similarity_score = compute_similarity(processed_resume, job_desc)
    ats_score = predict_resume_score(len(skills), 2, similarity_score)

    # Store in FAISS
    vector = get_resume_embedding(resume_text)
    index.add(np.array([vector]))
    faiss.write_index(index, "faiss_index.idx")

    # Store in SQLite
    c.execute("INSERT INTO resumes (name, skills, similarity_score, ats_score) VALUES (?, ?, ?, ?)",
              (resume_file.filename, ", ".join(skills), similarity_score, ats_score))
    conn.commit()

    return jsonify({
        "ats_score": ats_score,
        "skills": skills
    })

@app.route("/api/resumes", methods=["GET"])
@cross_origin(origins='http://localhost:3000', supports_credentials=True)
def get_all_resumes():
    c.execute("SELECT name, skills, similarity_score, ats_score FROM resumes")
    rows = c.fetchall()
    resumes = [{
        "name": row[0],
        "skills": row[1],
        "similarity_score": row[2],
        "ats_score": row[3]
    } for row in rows]
    return jsonify(resumes)

if __name__ == "__main__":
    app.run(debug=True)
