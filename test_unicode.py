#!/usr/bin/env python3
"""
Test Unicode mathematical symbols in questions
"""

import os
os.environ['GROQ_API_KEY'] = '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'

import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from textwrap import wrap

def generate_question(subject, topic):
    """Generate ONE test question with Unicode symbols"""
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Generate ONE GATE DA exam question.

Subject: {subject}
Topic: {topic}

CRITICAL: Use MATHEMATICAL SYMBOLS (Unicode)!
- Powers: x², x³, e⁻ᶻ (use superscripts: ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻)
- Greek: λ σ μ θ α β π Σ Δ Ω
- Operators: ≤ ≥ × ÷ √ ∈ ∞ ≠ ≈
- NOT: x^2, lambda, sqrt(), <=

Example (CORRECT):
Q. For X ~ N(μ=100, σ²=400), find P(90 ≤ X ≤ 110).

(A) 0.383
(B) 0.683
(C) 0.950
(D) 0.997

Answer: (B)

NOW GENERATE (with SYMBOLS):"""
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a GATE exam creator. ALWAYS use mathematical symbols: x², λ, σ, √, ≤, ≥, μ, π, ∈, ∞. NEVER use x^2, lambda, sqrt()."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 500
    }
    
    response = requests.post(API_URL, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()

# Test questions
print("🧪 Generating 2 test questions with Unicode symbols...\n")

questions = {}

# Question 1
print("📝 Probability and Statistics - Bayes Theorem...")
q1 = generate_question("Probability and Statistics", "Bayes Theorem")
questions["Probability"] = ("Bayes Theorem", q1)
print("✅ Generated!\n")
print("="*70)
print(q1)
print("="*70)
print()

# Question 2
print("📝 Linear Algebra - Eigenvalues...")
q2 = generate_question("Linear Algebra", "Eigenvalues and Eigenvectors")
questions["Linear Algebra"] = ("Eigenvalues", q2)
print("✅ Generated!\n")
print("="*70)
print(q2)
print("="*70)
print()

# Create PDF with Unicode support
print("\n📄 Creating PDF with Unicode support...")

# Try to load DejaVu font
try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuB', 'DejaVuSans-Bold.ttf'))
    font = 'DejaVu'
    font_bold = 'DejaVuB'
    print("✅ Using DejaVu font (full Unicode support)")
except:
    font = 'Helvetica'
    font_bold = 'Helvetica-Bold'
    print("⚠️ Using Helvetica (limited symbols)")

c = canvas.Canvas("test_unicode.pdf", pagesize=A4)
width, height = A4

# Title
c.setFont(font_bold, 16)
c.drawString(180, height - 60, "Test: Unicode Math Symbols")

y = height - 100

for i, (subject, (topic, question)) in enumerate(questions.items(), 1):
    if y < 150:
        c.showPage()
        y = height - 60
    
    # Header
    c.setFont(font_bold, 12)
    c.setFillColorRGB(0.2, 0.2, 0.6)
    c.drawString(60, y, f"{i}. {subject} - {topic}")
    y -= 20
    
    # Question
    c.setFont(font, 10)
    c.setFillColorRGB(0, 0, 0)
    
    for line in question.split('\n'):
        if line.strip():
            wrapped = wrap(line.strip(), 95)
            for wline in wrapped:
                if y < 100:
                    c.showPage()
                    c.setFont(font, 10)
                    y = height - 60
                
                try:
                    c.drawString(60, y, wline)
                except Exception as e:
                    print(f"⚠️ Error rendering: {wline[:50]}... - {e}")
                    c.drawString(60, y, wline.encode('ascii', 'replace').decode('ascii'))
                y -= 15
    
    y -= 10

c.save()
print("✅ PDF created: test_unicode.pdf")

import subprocess
subprocess.run(['start', 'test_unicode.pdf'], shell=True)

print("\n✅ CHECK THE PDF!")
print("   Look for: λ, σ, μ, ≤, ≥, ², ³, √")
print("   Should see symbols, not lambda/sigma/sqrt()")
