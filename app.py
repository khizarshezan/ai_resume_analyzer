# ============================================
# Project 4: AI-Powered Resume Analyzer
# ============================================

from flask import Flask, render_template, request, jsonify
import PyPDF2
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Khizar@Dev2024'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---- DATABASE CONFIG ----
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root1234',
    'database': 'khizar_portfolio'
}

# ---- SKILLS DATABASE ----
SKILL_KEYWORDS = {
    'Programming Languages': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'swift', 'kotlin', 'r'],
    'Web Development': ['html', 'css', 'react', 'angular', 'vue', 'node', 'flask', 'django', 'bootstrap'],
    'Data & Analytics': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'tableau', 'power bi', 'excel', 'sql'],
    'Databases': ['mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle', 'redis'],
    'Cloud & DevOps': ['aws', 'azure', 'docker', 'kubernetes', 'git', 'github', 'linux'],
    'Machine Learning': ['machine learning', 'deep learning', 'tensorflow', 'keras', 'scikit-learn', 'nlp', 'ai'],
}

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.lower()

def analyze_resume(resume_text, job_description):
    job_desc_lower = job_description.lower()
    resume_lower = resume_text.lower()

    matched_skills = {}
    missing_skills = {}

    for category, skills in SKILL_KEYWORDS.items():
        matched = [s for s in skills if s in resume_lower and s in job_desc_lower]
        missing = [s for s in skills if s in job_desc_lower and s not in resume_lower]
        if matched:
            matched_skills[category] = matched
        if missing:
            missing_skills[category] = missing

    total_job_skills = sum(len(s) for s in SKILL_KEYWORDS.values() if any(sk in job_desc_lower for sk in s))
    total_matched = sum(len(v) for v in matched_skills.values())
    match_score = round((total_matched / max(total_job_skills, 1)) * 100, 1)

    return matched_skills, missing_skills, match_score

def save_to_db(filename, job_title, match_score):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resume_analysis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                job_title VARCHAR(255),
                match_score FLOAT,
                analyzed_at DATETIME
            )
        """)
        cursor.execute("""
            INSERT INTO resume_analysis (filename, job_title, match_score, analyzed_at)
            VALUES (%s, %s, %s, %s)
        """, (filename, job_title, match_score, datetime.now()))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"DB Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['resume']
    job_description = request.form.get('job_description', '')
    job_title = request.form.get('job_title', '')

    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    resume_text = extract_text_from_pdf(filepath)
    matched_skills, missing_skills, match_score = analyze_resume(resume_text, job_description)

    save_to_db(file.filename, job_title, match_score)

    return jsonify({
        'match_score': match_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'filename': file.filename
    })

if __name__ == '__main__':
    app.run(debug=True)