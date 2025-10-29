#!/usr/bin/env python3
"""
Daily GATE Quiz Generator - 100% FREE!
Generates AI-powered questions and emails them to you and friends.
"""

import os
import json
import requests
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

# Load syllabus
with open('syllabus.json', 'r', encoding='utf-8') as f:
    SYLLABUS = json.load(f)

# Load or create progress tracker
try:
    with open('progress.json', 'r', encoding='utf-8') as f:
        progress = json.load(f)
except FileNotFoundError:
    progress = {subject: 0 for subject in SYLLABUS.keys()}
    print("📝 Created new progress tracker")

# Get credentials from environment variables (set in GitHub Secrets)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASS = os.getenv('GMAIL_PASS')
FRIENDS = os.getenv('FRIENDS', '').split(',') if os.getenv('FRIENDS') else []

# Validate environment variables
if not all([GROQ_API_KEY, GMAIL_USER, GMAIL_PASS]):
    raise ValueError("❌ Missing environment variables! Set GROQ_API_KEY, GMAIL_USER, and GMAIL_PASS")

print("✅ Configuration loaded successfully!")

# ============================================================================
# AI QUESTION GENERATION
# ============================================================================

def generate_all_questions_single_call(topic_list):
    """
    Generate ALL 8 questions in ONE API call - MUCH MORE EFFICIENT!
    
    Args:
        topic_list: List of (subject, topic) tuples
    
    Returns:
        List of (subject, topic, question_text) tuples
    """
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build the comprehensive prompt for all 8 questions
    topics_text = "\n".join([f"{i+1}. {subject}: {topic}" for i, (subject, topic) in enumerate(topic_list)])
    
    prompt = f"""Generate 8 challenging GATE DA (Data Science & AI) exam questions, ONE for each topic below.

TOPICS:
{topics_text}

FORMATTING RULES:
1. Write PROPER GATE exam questions with actual formulas and numbers
2. Use MATHEMATICAL SYMBOLS (Unicode):
   - Powers: x², x³, e⁻ᶻ (use superscripts: ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻)
   - Roots: √, ∛, ∜
   - Greek: α β γ δ θ λ μ σ π ω Σ Π Δ Ω
   - Operators: × ÷ ± ∓ ≠ ≈ ≤ ≥ ∞
   - Sets: ∈ ∉ ⊂ ⊆ ∪ ∩ ∅
   - Logic: ∀ ∃ ∧ ∨ ¬
3. Include NUMERICAL calculations and formulas
4. Keep questions CONCISE but clear (like real GATE papers)
5. GATE DA 2026 difficulty level

Format for EACH question:
=== QUESTION [NUMBER] ===
Q. [Question with actual numbers and formulas using symbols]

(A) [Option with numbers]
(B) [Option with numbers]
(C) [Option with numbers]
(D) [Option with numbers]

Answer: (X)

Generate ALL 8 questions now:"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are a GATE DA exam question creator. Write CONCISE questions with actual numbers and formulas. Use MATHEMATICAL SYMBOLS: x², λ, σ, √, ≤, ≥, ∈, ∞, α, β, θ, μ, π, Σ. Keep questions short and precise like real GATE papers."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 4000,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    try:
        print("🤖 Making ONE API call for all 8 questions...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                generated_text = result['choices'][0]['message']['content']
                
                # Parse the generated questions
                questions = []
                question_blocks = generated_text.split("=== QUESTION")
                
                for i, (subject, topic) in enumerate(topic_list):
                    # Try to find the corresponding question block
                    question_text = None
                    for block in question_blocks:
                        if f"{i+1}" in block[:10]:  # Check if this is question i+1
                            # Extract everything after the === line
                            lines = block.split("\n", 1)
                            if len(lines) > 1:
                                question_text = lines[1].strip()
                                break
                    
                    # Fallback if parsing fails
                    if not question_text:
                        question_text = f"""Q. In {topic}, which of the following is TRUE?

(A) Option A
(B) Option B
(C) Option C
(D) Option D

Answer: (A)"""
                    
                    questions.append((subject, topic, question_text))
                
                print(f"✅ Generated {len(questions)} questions in ONE API call!")
                return questions
        
        print(f"❌ API error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error in single API call: {str(e)}")
    
    # Fallback: Use old method (8 separate calls)
    print("⚠️ Falling back to individual API calls...")
    return [(subj, top, generate_question(subj, top)) for subj, top in topic_list]

def generate_question(subject, topic, retry_count=3):
    """
    Generate a GATE-level question using Groq API (FREE & SUPER FAST!)
    
    Args:
        subject: Subject name (e.g., "Probability & Statistics")
        topic: Specific topic (e.g., "Bayes Theorem")
        retry_count: Number of retries if API fails
    
    Returns:
        Generated question text with LaTeX formatting
    """
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Generate ONE challenging GATE DA (Data Science & AI) exam question.

Subject: {subject}
Topic: {topic}

FORMATTING RULES:
1. Write PROPER GATE exam questions with actual formulas and numbers
2. Use MATHEMATICAL SYMBOLS (Unicode):
   - Powers: x², x³, e⁻ᶻ (use superscripts: ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻)
   - Roots: √, ∛, ∜
   - Greek: α β γ δ θ λ μ σ π ω Σ Π Δ Ω
   - Operators: × ÷ ± ∓ ≠ ≈ ≤ ≥ ∞
   - Sets: ∈ ∉ ⊂ ⊆ ∪ ∩ ∅
   - Logic: ∀ ∃ ∧ ∨ ¬
   - Fractions: Use / or write as "a/b"
3. Include NUMERICAL calculations and formulas
4. Keep questions CONCISE but clear (like real GATE papers)
5. GATE DA 2026 difficulty level

Format:
Q. [Question with actual numbers and formulas using symbols]

(A) [Option with numbers]
(B) [Option with numbers]
(C) [Option with numbers]
(D) [Option with numbers]

Answer: (X)

GOOD Examples:

Example 1 (Bayes):
Q. A medical test has sensitivity 0.95 and specificity 0.98. If disease prevalence is 1%, what is P(Disease|Positive) using Bayes' theorem?

(A) 0.324
(B) 0.487
(C) 0.657
(D) 0.950

Answer: (A)

Example 2 (Linear Algebra):
Q. Matrix A = [[2,1],[1,2]] has eigenvalues λ₁ and λ₂. What is det(A - 3I)?

(A) -5
(B) 0
(C) 3
(D) 5

Answer: (B)

Example 3 (Statistics):
Q. For X ~ N(μ=50, σ²=25), what is P(45 ≤ X ≤ 55)?

(A) 0.68
(B) 0.95
(C) 0.997
(D) 1.0

Answer: (A)

Example 4 (ML):
Q. Logistic regression uses sigmoid σ(z) = 1/(1 + e⁻ᶻ). If z = 3, find σ(z) given e⁻³ = 0.05.

(A) 0.90
(B) 0.95
(C) 0.98
(D) 0.99

Answer: (B)

NOW GENERATE (concise GATE question with real mathematical symbols):"""

    payload = {
        "model": "llama-3.3-70b-versatile",  # Latest, fastest, FREE!
        "messages": [
            {
                "role": "system",
                "content": "You are a GATE DA exam question creator. Write CONCISE questions with actual numbers and formulas. Use MATHEMATICAL SYMBOLS: x², λ, σ, √, ≤, ≥, ∈, ∞, α, β, θ, μ, π, Σ. Keep questions short and precise like real GATE papers."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    for attempt in range(retry_count):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    generated_text = result['choices'][0]['message']['content']
                    # Extract only the generated part (remove any extra text)
                    if "NOW GENERATE:" in generated_text:
                        question = generated_text.split("NOW GENERATE:")[-1].strip()
                    else:
                        question = generated_text.strip()
                    return question
                else:
                    print(f"⚠️ Unexpected API response format")
            else:
                print(f"⚠️ API error: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"⚠️ Error generating question (attempt {attempt + 1}/{retry_count}): {str(e)}")
        
        if attempt < retry_count - 1:
            time.sleep(2)  # Groq is fast, shorter wait
    
    # Fallback question if API fails
    return f"""Q. In {topic}, which of the following statements is TRUE?

(A) Statement A related to {topic}
(B) Statement B related to {topic}
(C) Statement C related to {topic}
(D) All of the above

Answer: (D)

[Note: This is a fallback question. Check API configuration if you see this.]"""

# ============================================================================
# PDF GENERATION (Using ReportLab)
# ============================================================================

def create_pdf(questions, filename='quiz.pdf'):
    """Create PDF using ReportLab with Unicode support"""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # Register DejaVu fonts (supports Unicode math symbols)
    try:
        pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVu-Italic', 'DejaVuSans-Oblique.ttf'))
        font_family = 'DejaVu'
    except:
        # Fallback to Helvetica if DejaVu not available
        font_family = 'Helvetica'
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont(f"{font_family}-Bold" if font_family == 'DejaVu' else "Helvetica-Bold", 16)
    c.drawString(200, height - 60, "GATE DA Daily Practice Quiz")
    
    # Date
    c.setFont(font_family, 10)
    date_str = datetime.now().strftime("%B %d, %Y")
    c.drawString(250, height - 80, date_str)
    
    # Motivational text
    c.setFont(f"{font_family}-Italic" if font_family == 'DejaVu' else "Helvetica-Oblique", 11)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawCentredString(width/2, height - 100, "Solve all questions before checking answers at the bottom!")
    
    y = height - 140
    
    # Add questions
    for i, (subject, (topic, question)) in enumerate(questions.items(), 1):
        # Check if we need a new page
        if y < 150:
            c.showPage()
            c.setFont(font_family, 12)
            y = height - 60
        
        # Question header
        c.setFont(f"{font_family}-Bold" if font_family == 'DejaVu' else "Helvetica-Bold", 13)
        c.setFillColorRGB(0.2, 0.2, 0.6)
        header = f"{i}. {subject} - {topic}"
        c.drawString(60, y, header)
        y -= 20
        
        # Question text
        c.setFont(font_family, 10)
        c.setFillColorRGB(0, 0, 0)
        
        lines = question.split('\n')
        for line in lines:
            if line.strip() and not line.strip().startswith('Answer:'):
                # Wrap long lines
                wrapped_lines = wrap(line.strip(), 95)
                for wline in wrapped_lines:
                    if y < 100:
                        c.showPage()
                        c.setFont(font_family, 10)
                        y = height - 60
                    
                    try:
                        c.drawString(60, y, wline)
                    except:
                        # Fallback if Unicode fails
                        c.drawString(60, y, wline.encode('ascii', 'replace').decode('ascii'))
                    y -= 15
        
        y -= 10
    
    # Add separator before answers
    y -= 10
    if y < 200:
        c.showPage()
        y = height - 60
    
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.line(60, y, width - 60, y)
    y -= 20
    
    # Answers section
    c.setFont(f"{font_family}-Bold" if font_family == 'DejaVu' else "Helvetica-Bold", 14)
    c.setFillColorRGB(0.8, 0.2, 0.2)
    c.drawCentredString(width/2, y, "ANSWERS (Check after solving!)")
    y -= 25
    
    c.setFont(font_family, 10)
    c.setFillColorRGB(0, 0, 0)
    
    for i, (subject, (topic, question)) in enumerate(questions.items(), 1):
        if y < 100:
            c.showPage()
            c.setFont(font_family, 10)
            y = height - 60
        
        # Extract answer
        answer_line = "Answer not found"
        for line in question.split('\n'):
            if line.strip().startswith('Answer:'):
                answer_line = line.strip()
                break
        
        try:
            c.drawString(60, y, f"{i}. {subject}: {answer_line}")
        except:
            c.drawString(60, y, f"{i}. {subject}: {answer_line}".encode('ascii', 'replace').decode('ascii'))
        y -= 18
    
    c.save()
    print(f"✅ PDF created: {filename}")
    return filename

# ============================================================================
# PROGRESS VISUALIZATION
# ============================================================================"""
# EMAIL DELIVERY
# ============================================================================

def send_email(pdf_file, questions):
    """
    Send quiz email via Gmail (FREE!)
    
    Args:
        pdf_file: Path to PDF file
        questions: Dict of questions for email body
    """
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    msg['Subject'] = f"Daily DA 2026 Quiz - {datetime.now().strftime('%b %d, %Y')}"
    
    # Email body
    topics_list = '\n'.join([f"  • {subj}: {topic}" for subj, (topic, _) in questions.items()])
    
    body = f"""Hello DA 2026 Warrior!

Your daily dose of challenging questions is ready!

Today's High-Weightage Topics:
{topics_list}
---
Powered by FREE AI (Groq + GitHub Actions)
Keep grinding! DA 2026 is yours!looking at answers first!
- These topics are frequently asked in DA exams
- Practice similar variations for better understanding

Good luck and happy learning!

---
Powered by FREE AI (Hugging Face + GitHub Actions)
Keep grinding! DA 2026 is yours!
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach PDF
    try:
        with open(pdf_file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={pdf_file}')
            msg.attach(part)
    except Exception as e:
        print(f"⚠️ Error attaching PDF: {e}")
        return
    
    # Prepare recipient list (you + friends)
    recipients = [GMAIL_USER] + [email.strip() for email in FRIENDS if email.strip()]
    
    # Send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg, to_addrs=recipients)
        
        print(f"✅ Email sent successfully to {len(recipients)} recipient(s)!")
        print(f"   Recipients: {', '.join(recipients)}")
    
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("DAILY DA 2026 QUIZ GENERATOR - OPTIMIZED!")
    print("="*60 + "\n")
    
    # Collect topics for today
    topic_list = []
    
    print("📋 Selecting today's topics...\n")
    
    for subject, topics in SYLLABUS.items():
        # Get current topic index (cycles through topics)
        topic_index = progress[subject] % len(topics)
        topic = topics[topic_index]
        topic_list.append((subject, topic))
        print(f"  • {subject}: {topic}")
        
        # Update progress for next day
        progress[subject] = topic_index + 1
    
    # Generate ALL questions in ONE API call - MUCH BETTER!
    print(f"\n🚀 Generating all {len(topic_list)} questions in ONE API call...\n")
    question_tuples = generate_all_questions_single_call(topic_list)
    
    # Convert to the format expected by create_pdf
    questions = {}
    for subject, topic, question_text in question_tuples:
        questions[subject] = (topic, question_text)
    
    print(f"\n✅ Generated {len(questions)} questions!\n")
    
    # Create PDF
    print("📄 Creating PDF...")
    pdf_file = create_pdf(questions)
    
    # Send email
    print("📧 Sending email...")
    send_email(pdf_file, questions)
    
    # Save progress
    with open('progress.json', 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)
    
    print("\n" + "="*60)
    print("SUCCESS! Check your email!")
    print("="*60 + "\n")
    
    # Print summary
    print("Summary:")
    print(f"  * Questions generated: {len(questions)}")
    print(f"  * PDF created: {pdf_file}")
    print(f"  * Topics covered today:")
    for subject, (topic, _) in questions.items():
        print(f"    - {subject}: {topic}")
    print("\n💡 ONE API call = 8x more efficient!")
    print("Keep grinding! DA 2026 is yours!\n")

if __name__ == "__main__":
    main()
