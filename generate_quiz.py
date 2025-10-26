#!/usr/bin/env python3
"""
Daily GATE Quiz Generator - 100% FREE!
Generates AI-powered questions and emails them to you and friends.
"""

import os
import json
import requests
from datetime import datetime
from fpdf import FPDF  # fpdf2 package, imports as 'fpdf'
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
2. Use SIMPLE ASCII math notation:
   - Powers: x^2, x^3, e^(-z)
   - Fractions: 1/2, (a+b)/c
   - Multiplication: * or just write "2x"
   - Division: / or ÷
   - Greek letters: spell them out (lambda, sigma, theta, alpha, beta, mu)
   - Comparisons: <=, >=, !=, ~=
   - Special: sqrt(), sum(), infinity
3. Include NUMERICAL calculations and formulas
4. Keep questions CONCISE but clear (like real GATE papers)
5. GATE DA 2026 difficulty level

Format:
Q. [Question with actual numbers and formulas]

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
Q. Matrix A = [[2,1],[1,2]] has eigenvalues lambda_1 and lambda_2. What is det(A - 3I)?

(A) -5
(B) 0
(C) 3
(D) 5

Answer: (B)

Example 3 (Statistics):
Q. For X ~ N(mu=50, sigma^2=25), what is P(45 <= X <= 55)?

(A) 0.68
(B) 0.95
(C) 0.997
(D) 1.0

Answer: (A)

Example 4 (ML):
Q. Logistic regression uses sigmoid sigma(z) = 1/(1 + e^(-z)). If z = 3, find sigma(z) given e^(-3) = 0.05.

(A) 0.90
(B) 0.95
(C) 0.98
(D) 0.99

Answer: (B)

BAD Example (Too wordy):
Q. In a medical diagnosis scenario where a patient is suspected to have a certain disease and the probability...

NOW GENERATE (concise GATE question with real numbers):"""

    payload = {
        "model": "llama-3.3-70b-versatile",  # Latest, fastest, FREE!
        "messages": [
            {
                "role": "system",
                "content": "You are a GATE DA exam question creator. Write CONCISE questions with actual numbers and formulas. Use simple ASCII notation: x^2, lambda, sigma, sqrt(), <=, >=. Keep questions short and precise like real GATE papers."
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
# PDF GENERATION
# ============================================================================

class QuizPDF(FPDF):
    """Custom PDF class for quiz generation"""
    
    def header(self):
        """PDF Header with title and date"""
        self.set_font('helvetica', 'B', 18)
        self.set_text_color(255, 107, 53)  # Orange color
        self.cell(0, 10, 'Daily DA 2026 Quiz', 0, 1, 'C')
        
        self.set_font('helvetica', '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, datetime.now().strftime('%B %d, %Y'), 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """PDF Footer"""
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Generated with AI - Good luck!', 0, 0, 'C')

def create_pdf(questions):
    """
    Create a professionally formatted PDF with all questions
    
    Args:
        questions: Dict of {subject: (topic, question_text)}
    
    Returns:
        Filename of generated PDF
    """
    try:
        pdf = QuizPDF()
        pdf.add_page()
        
        # Add motivational header
        pdf.set_font('helvetica', 'I', 11)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 6, 'Solve all questions before checking answers at the bottom!', 0, 'C')
        pdf.ln(8)
        
        # Add questions
        for i, (subject, (topic, question)) in enumerate(questions.items(), 1):
            # Subject header
            pdf.set_font('helvetica', 'B', 13)
            pdf.set_text_color(50, 50, 150)
            pdf.cell(0, 8, f"{i}. {subject} - {topic}", 0, 1)
            
            # Question text
            pdf.set_font('helvetica', '', 10)
            pdf.set_text_color(0, 0, 0)
            
            # Use write() instead of multi_cell - better for long lines
            for line in question.split('\n'):
                line = line.strip()
                if line:
                    try:
                        pdf.write(5, line)
                        pdf.ln()
                    except Exception as e:
                        print(f"⚠️ Skipped line: {str(e)[:60]}")
            
            pdf.ln(5)
        
        # Add separator before answers
        pdf.ln(10)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Answers section
        pdf.set_font('helvetica', 'B', 14)
        pdf.set_text_color(200, 50, 50)
        pdf.cell(0, 10, 'ANSWERS (Check after solving!)', 0, 1, 'C')
        pdf.ln(3)
        
        pdf.set_font('helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        for i, (subject, (topic, question)) in enumerate(questions.items(), 1):
            # Extract answer from question text
            answer_line = "Answer not found"
            for line in question.split('\n'):
                if line.strip().startswith('Answer:'):
                    answer_line = line.strip()
                    break
            
            try:
                pdf.cell(0, 6, f"{i}. {subject}: {answer_line}", 0, 1)
            except Exception as e:
                print(f"⚠️ Skipped answer for {subject}: {e}")
                pdf.cell(0, 6, f"{i}. {subject}: See questions above", 0, 1)
        
        # Save PDF
        filename = f"da_quiz_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf.output(filename)
        print(f"📄 PDF created: {filename}")
        
        return filename
    
    except Exception as e:
        print(f"❌ Error creating PDF: {str(e)}")
        print(f"📝 Full error details: {repr(e)}")
        raise

# ============================================================================
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
    print("DAILY DA 2026 QUIZ GENERATOR - 100% FREE!")
    print("="*60 + "\n")
    
    questions = {}
    
    # Generate questions for each subject
    print("Generating AI-powered questions...\n")
    
    for subject, topics in SYLLABUS.items():
        # Get current topic index (cycles through topics)
        topic_index = progress[subject] % len(topics)
        topic = topics[topic_index]
        
        print(f"[{subject}] {topic}...")
        question = generate_question(subject, topic)
        questions[subject] = (topic, question)
        
        # Update progress for next day
        progress[subject] = topic_index + 1
        
        # Small delay to avoid API rate limits
        time.sleep(2)
    
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
    print("\nKeep grinding! DA 2026 is yours!\n")

if __name__ == "__main__":
    main()
