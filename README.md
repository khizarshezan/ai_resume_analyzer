# AI-Powered Resume Analyzer

## Overview
A web application that analyzes resumes against job descriptions and provides a match score with detailed skill gap analysis.

## Features
- Upload resume as PDF
- Paste any job description
- Get instant match score (0-100%)
- See matched and missing skills by category
- Results saved to MySQL database

## Tech Stack
- **Python** — Backend logic
- **Flask** — Web framework
- **PyPDF2** — PDF text extraction
- **MySQL** — Store analysis results
- **Bootstrap** — Frontend styling

## How to Run
1. Install requirements: `pip install flask PyPDF2 mysql-connector-python`
2. Start MySQL service
3. Run `python app.py`
4. Open `http://localhost:5000`
