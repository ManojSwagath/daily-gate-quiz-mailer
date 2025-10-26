#!/usr/bin/env python3
"""
Quick test - Generate 3 questions to verify readability
"""

import os
os.environ['GROQ_API_KEY'] = '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'
os.environ['GMAIL_USER'] = 'a.manojswagath@gmail.com'
os.environ['GMAIL_PASS'] = 'ziln shde xrts rvre'
os.environ['FRIENDS'] = ''

import json
import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
from datetime import datetime

# Load syllabus
with open('syllabus.json', 'r') as f:
    SYLLABUS = json.load(f)

def generate_test_question(subject, topic):
    """Generate ONE test question"""
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Generate ONE GATE DA exam question.

Subject: {subject}
Topic: {topic}

Use CONCISE language with ACTUAL numbers and formulas!
Use simple ASCII: x^2, lambda, sigma, <=, >=, sqrt()

Example:
Q. For X ~ N(mu=100, sigma^2=400), find P(90 < X < 110).

(A) 0.383
(B) 0.683
(C) 0.950
(D) 0.997

Answer: (B)

NOW GENERATE (short question with real math):"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a GATE exam creator. Write SHORT, PRECISE questions with real numbers and formulas using simple ASCII: x^2, lambda, sigma, sqrt(), <=, >=. NO Unicode symbols. Keep it concise like actual GATE papers."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except:
        pass
    
    return f"Q. Test question on {topic}\n\n(A) A\n(B) B\n(C) C\n(D) D\n\nAnswer: (A)"

# Generate 3 test questions
print("🧪 Generating 3 test questions...\n")

test_subjects = [
    ("Probability and Statistics", "Bayes Theorem"),
    ("Linear Algebra", "Eigenvalues and Eigenvectors"),
    ("Machine Learning - Supervised", "Logistic Regression")
]

questions = {}
for subject, topic in test_subjects:
    print(f"📝 {subject} - {topic}...")
    q = generate_test_question(subject, topic)
    questions[subject] = (topic, q)
    print(f"✅ Generated!\n")
    print("="*70)
    print(q)
    print("="*70)
    print()

# Create PDF using ReportLab
print("\n📄 Creating test PDF...")

c = canvas.Canvas("test_quiz_readable.pdf", pagesize=A4)
width, height = A4

# Title
c.setFont("Helvetica-Bold", 16)
c.drawString(200, height - 60, "GATE DA Test Quiz - Readability Check")

y = height - 100

for i, (subject, (topic, question)) in enumerate(questions.items(), 1):
    # Check if we need a new page
    if y < 150:
        c.showPage()
        c.setFont("Helvetica", 12)
        y = height - 60
    
    # Question header
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0, 0, 0.6)
    header = f"{i}. {subject} - {topic}"
    c.drawString(60, y, header)
    y -= 20
    
    # Question text
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 0)
    
    lines = question.split('\n')
    for line in lines:
        if line.strip():
            # Wrap long lines
            wrapped_lines = wrap(line, 95)
            for wline in wrapped_lines:
                if y < 100:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = height - 60
                
                c.drawString(60, y, wline)
                y -= 15
    
    y -= 10

c.save()
print("✅ PDF created: test_quiz_readable.pdf")
print("\n📂 Opening PDF...")

import subprocess
subprocess.run(['start', 'test_quiz_readable.pdf'], shell=True)

print("\n✅ CHECK THE PDF!")
print("   Questions should be 100% readable now!")
print("   No $ symbols, no weird LaTeX!")
