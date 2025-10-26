#!/usr/bin/env python3
"""
Daily GATE Quiz Generator - 100% FREE!
Generates AI-powered questions and emails them to you and friends.
"""

import os
import json
import requests
from datetime import datetime
from fpdf import FPDF
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
HF_TOKEN = os.getenv('HF_TOKEN')
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASS = os.getenv('GMAIL_PASS')
FRIENDS = os.getenv('FRIENDS', '').split(',') if os.getenv('FRIENDS') else []

# Validate environment variables
if not all([HF_TOKEN, GMAIL_USER, GMAIL_PASS]):
    raise ValueError("❌ Missing environment variables! Set HF_TOKEN, GMAIL_USER, and GMAIL_PASS")

print("✅ Configuration loaded successfully!")

# ============================================================================
# AI QUESTION GENERATION
# ============================================================================

def generate_question(subject, topic, retry_count=3):
    """
    Generate a GATE-level question using Hugging Face API (FREE!)
    
    Args:
        subject: Subject name (e.g., "Algorithms")
        topic: Specific topic (e.g., "Dynamic Programming")
        retry_count: Number of retries if API fails
    
    Returns:
        Generated question text with LaTeX formatting
    """
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    prompt = f"""Generate ONE extremely challenging DA/GATE Computer Science exam question.

Subject: {subject}
Topic: {topic}

Requirements:
1. DA 2026 exam difficulty level (top 10% hardest questions)
2. Use LaTeX for math: $x^2$ for inline, $$equation$$ for block
3. Four options (A, B, C, D) with ONE correct answer
4. Include tricky reasoning that tests deep conceptual understanding
5. Focus on frequently asked exam patterns
6. Add numerical values or specific scenarios where applicable

Format (STRICT):
Q. [Your challenging question here with LaTeX if needed]

(A) [First option]
(B) [Second option]
(C) [Third option]
(D) [Fourth option]

Answer: (X)

Example for Dynamic Programming:
Q. Consider the 0/1 Knapsack problem with capacity $W = 10$ and items with weights $[2, 3, 4, 5]$ and values $[3, 4, 5, 6]$. What is the maximum value achievable?

(A) 10
(B) 11
(C) 12
(D) 13

Answer: (D)

NOW GENERATE for DA 2026 exam:"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }
    
    for attempt in range(retry_count):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0]['generated_text']
                    # Extract only the generated part (remove prompt)
                    question = generated_text.split("NOW GENERATE:")[-1].strip()
                    return question
                else:
                    print(f"⚠️ Unexpected API response format")
            elif response.status_code == 503:
                # Model is loading, wait and retry
                print(f"⏳ Model loading... waiting 20 seconds (attempt {attempt + 1}/{retry_count})")
                time.sleep(20)
                continue
            else:
                print(f"⚠️ API error: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"⚠️ Error generating question (attempt {attempt + 1}/{retry_count}): {str(e)}")
        
        if attempt < retry_count - 1:
            time.sleep(5)  # Wait before retry
    
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
        self.set_font('Arial', 'B', 18)
        self.set_text_color(255, 107, 53)  # Orange color
        self.cell(0, 10, '🔥 Daily DA 2026 Quiz', 0, 1, 'C')
        
        self.set_font('Arial', '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, datetime.now().strftime('%B %d, %Y'), 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """PDF Footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Generated with ❤️ by FREE AI - Good luck! 🎓', 0, 0, 'C')

def create_pdf(questions):
    """
    Create a professionally formatted PDF with all questions
    
    Args:
        questions: Dict of {subject: (topic, question_text)}
    
    Returns:
        Filename of generated PDF
    """
    pdf = QuizPDF()
    pdf.add_page()
    
    # Add motivational header
    pdf.set_font('Arial', 'I', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, 'Solve all questions before checking answers at the bottom! 💪', 0, 'C')
    pdf.ln(8)
    
    # Add questions
    for i, (subject, (topic, question)) in enumerate(questions.items(), 1):
        # Subject header
        pdf.set_font('Arial', 'B', 13)
        pdf.set_text_color(50, 50, 150)
        pdf.cell(0, 8, f"{i}. {subject} - {topic}", 0, 1)
        
        # Question text
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        # Split question by lines and handle LaTeX markers
        question_lines = question.split('\n')
        for line in question_lines:
            if line.strip():
                pdf.multi_cell(0, 5, line)
        
        pdf.ln(5)
    
    # Add separator before answers
    pdf.ln(10)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Answers section
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(200, 50, 50)
    pdf.cell(0, 10, '📝 ANSWERS (Check after solving!)', 0, 1, 'C')
    pdf.ln(3)
    
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0)
    
    for i, (subject, (topic, question)) in enumerate(questions.items(), 1):
        # Extract answer from question text
        answer_line = "Answer not found"
        for line in question.split('\n'):
            if line.strip().startswith('Answer:'):
                answer_line = line.strip()
                break
        
        pdf.cell(0, 6, f"{i}. {subject}: {answer_line}", 0, 1)
    
    # Save PDF
    filename = f"da_quiz_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf.output(filename)
    print(f"📄 PDF created: {filename}")
    
    return filename

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
    msg['Subject'] = f"🔥 Daily DA 2026 Quiz - {datetime.now().strftime('%b %d, %Y')}"
    
    # Email body
    topics_list = '\n'.join([f"  • {subj}: {topic}" for subj, (topic, _) in questions.items()])
    
    body = f"""Hello DA 2026 Warrior! 💪

Your daily dose of challenging questions is ready!

📚 Today's High-Weightage Topics:
{topics_list}

💡 Pro tips: 
- Attempt all questions without looking at answers first!
- These topics are frequently asked in DA exams
- Practice similar variations for better understanding

Good luck and happy learning! 🎓

---
Powered by FREE AI (Hugging Face + GitHub Actions)
Keep grinding! DA 2026 is yours! 🔥
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
    print("🔥 DAILY DA 2026 QUIZ GENERATOR - 100% FREE!")
    print("="*60 + "\n")
    
    questions = {}
    
    # Generate questions for each subject
    print("🤖 Generating AI-powered questions...\n")
    
    for subject, topics in SYLLABUS.items():
        # Get current topic index (cycles through topics)
        topic_index = progress[subject] % len(topics)
        topic = topics[topic_index]
        
        print(f"📚 {subject} - {topic}...")
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
    print("🎉 SUCCESS! Check your email!")
    print("="*60 + "\n")
    
    # Print summary
    print("📊 Summary:")
    print(f"  • Questions generated: {len(questions)}")
    print(f"  • PDF created: {pdf_file}")
    print(f"  • Topics covered today:")
    for subject, (topic, _) in questions.items():
        print(f"    - {subject}: {topic}")
    print("\n💪 Keep grinding! DA 2026 is yours! 🔥\n")

if __name__ == "__main__":
    main()
