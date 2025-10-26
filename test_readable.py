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
from fpdf import FPDF
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

CRITICAL: Write like a REAL EXAM QUESTION - natural, clear language!

For math: Use words like "squared", "raised to power", "divided by", etc.
Make it sound like a professor asking a question, not code.

Format:
Q. [Natural exam-style question - explain clearly]

(A) Descriptive option A
(B) Descriptive option B  
(C) Descriptive option C
(D) Descriptive option D

Answer: (X)

GOOD Example:
Q. A classifier achieves 95% accuracy on a test set of 1000 samples where 10% of samples belong to the positive class. If the classifier predicts all samples as negative class, what would be its accuracy on this same test set?

(A) 85%
(B) 90%
(C) 95%
(D) 100%

Answer: (B)

NOW GENERATE (natural exam language):"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a GATE exam question creator. Write questions in natural, exam-like language. Use descriptive words instead of symbols. Make it sound like a real professor asking a challenging question."},
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

# Create PDF
print("\n📄 Creating test PDF...")

class TestPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, 'GATE DA Test Quiz - Readability Check', 0, 1, 'C')
        self.ln(5)

pdf = TestPDF()
pdf.add_page()

for i, (subject, (topic, question)) in enumerate(questions.items(), 1):
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(0, 0, 150)
    pdf.cell(0, 8, f"{i}. {subject} - {topic}", 0, 1)
    
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    
    for line in question.split('\n'):
        if line.strip():
            # Use write() instead of multi_cell for better compatibility
            pdf.write(5, line.strip())
            pdf.ln()
    
    pdf.ln(5)

pdf.output('test_quiz_readable.pdf')
print("✅ PDF created: test_quiz_readable.pdf")
print("\n📂 Opening PDF...")

import subprocess
subprocess.run(['start', 'test_quiz_readable.pdf'], shell=True)

print("\n✅ CHECK THE PDF!")
print("   Questions should be 100% readable now!")
print("   No $ symbols, no weird LaTeX!")
