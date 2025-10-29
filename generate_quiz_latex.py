#!/usr/bin/env python3
"""
Daily GATE Quiz Generator with LaTeX - For GitHub Actions
Generates AI-powered questions with LaTeX and emails beautiful PDFs
"""

import os
import json
import requests
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time
import subprocess
import tempfile

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

# Get credentials from environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASS = os.getenv('GMAIL_PASS')
FRIENDS = os.getenv('FRIENDS', '').split(',') if os.getenv('FRIENDS') else []

# Validate environment variables
if not all([GROQ_API_KEY, GMAIL_USER, GMAIL_PASS]):
    raise ValueError("❌ Missing environment variables! Set GROQ_API_KEY, GMAIL_USER, and GMAIL_PASS")

print("✅ Configuration loaded successfully!")

# ============================================================================
# AI QUESTION GENERATION WITH LATEX - ONE API CALL
# ============================================================================

def generate_all_questions_latex(topic_list):
    """
    Generate ALL 8 questions in one API call with LaTeX formatting
    More efficient and cleaner approach!
    """
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build the topics description
    topics_text = "\n".join([f"{i+1}. {subject} - {topic}" for i, (subject, topic) in enumerate(topic_list)])
    
    prompt = f"""Generate 8 CHALLENGING GATE DA exam questions with ADVANCED LaTeX mathematical notation for these topics:

{topics_text}

CRITICAL REQUIREMENTS:
1. Generate EXACTLY 8 questions (one for each topic above)
2. Use ADVANCED mathematical notation with proper LaTeX
3. Include COMPLEX math symbols:
   - Integrals: $\\int_{{a}}^{{b}} f(x)dx$ or $$\\int_{{0}}^{{\\infty}} e^{{-x}} dx$$
   - Summations: $\\sum_{{i=1}}^{{n}} x_i$
   - Limits: $\\lim_{{x \\to 0}} \\frac{{\\sin(x)}}{{x}}$
   - Partial derivatives: $\\frac{{\\partial f}}{{\\partial x}}$
   - Fractions: $\\frac{{numerator}}{{denominator}}$
   - Matrices: $\\begin{{bmatrix}} a & b \\\\ c & d \\end{{bmatrix}}$
   - Greek letters: $\\lambda$, $\\sigma$, $\\mu$, $\\theta$, $\\alpha$, $\\beta$, $\\pi$
4. Make questions CHALLENGING with actual numerical calculations
5. Use display math ($$...$$) for complex expressions

FORMAT FOR EACH QUESTION (EXACTLY):

=== Question N: [Subject] - [Topic] ===

Q. [Challenging question with advanced LaTeX notation]

(A) [Option with proper notation]
(B) [Option with proper notation]
(C) [Option with proper notation]
(D) [Option with proper notation]

Answer: (X)

Explanation: [Detailed explanation with step-by-step LaTeX formulas]

===

EXAMPLE WITH ADVANCED MATH:

=== Question 1: Calculus - Integration ===

Q. Evaluate the definite integral $$\\int_{{0}}^{{\\pi}} \\sin^2(x) dx$$ using the identity $\\sin^2(x) = \\frac{{1 - \\cos(2x)}}{{2}}$.

(A) $\\frac{{\\pi}}{{4}}$
(B) $\\frac{{\\pi}}{{2}}$
(C) $\\pi$
(D) $2\\pi$

Answer: (B)

Explanation: Using the identity, we have:
$$\\int_{{0}}^{{\\pi}} \\sin^2(x) dx = \\int_{{0}}^{{\\pi}} \\frac{{1 - \\cos(2x)}}{{2}} dx = \\frac{{1}}{{2}}\\left[x - \\frac{{\\sin(2x)}}{{2}}\\right]_{{0}}^{{\\pi}} = \\frac{{\\pi}}{{2}}$$

===

NOW GENERATE ALL 8 QUESTIONS with ADVANCED MATH like above:"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert GATE DA exam question creator. Generate CHALLENGING questions with ADVANCED LaTeX mathematical notation including integrals, summations, matrices, complex fractions, limits, and partial derivatives. Use $ for inline math, $$ for display math. Follow the exact format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 4000,  # Enough for 8 questions
        "temperature": 0.7
    }
    
    try:
        print("🤖 Generating all 8 questions in one API call...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                full_response = result['choices'][0]['message']['content'].strip()
                return parse_questions(full_response, topic_list)
            else:
                print(f"⚠️ Unexpected API response format")
                return None
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        print(f"❌ Error generating questions: {str(e)}")
        return None


def parse_questions(full_response, topic_list):
    """
    Parse the AI response into individual questions
    """
    questions = []
    
    # Split by === markers
    parts = full_response.split('===')
    
    # Filter out empty parts and extract questions
    question_blocks = [part.strip() for part in parts if part.strip() and 'Question' in part]
    
    if len(question_blocks) >= len(topic_list):
        for i, (subject, topic) in enumerate(topic_list):
            if i < len(question_blocks):
                # Remove the header line "Question N: Subject - Topic"
                question_text = question_blocks[i]
                lines = question_text.split('\n', 1)
                if len(lines) > 1:
                    question_content = lines[1].strip()
                else:
                    question_content = question_text
                
                questions.append((subject, topic, question_content))
    else:
        print(f"⚠️ Only got {len(question_blocks)} questions, expected {len(topic_list)}")
        # Use fallback for missing questions
        for i, (subject, topic) in enumerate(topic_list):
            if i < len(question_blocks):
                question_text = question_blocks[i]
                lines = question_text.split('\n', 1)
                question_content = lines[1].strip() if len(lines) > 1 else question_text
                questions.append((subject, topic, question_content))
            else:
                # Fallback question
                fallback = f"""Q. In {topic}, which statement is TRUE?

(A) Statement A
(B) Statement B
(C) Statement C
(D) All of the above

Answer: (D)

Explanation: [Fallback question - check API]"""
                questions.append((subject, topic, fallback))
    
    return questions

# ============================================================================
# LATEX PDF GENERATION
# ============================================================================

def create_latex_document(questions):
    """Create complete LaTeX document"""
    latex_content = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{titlesec}

% Custom formatting
\titleformat{\section}
  {\normalfont\Large\bfseries\color{blue!70!black}}
  {\thesection}{1em}{}

\setlength{\parindent}{0pt}
\setlength{\parskip}{10pt}

\begin{document}

\begin{center}
    {\LARGE \textbf{GATE DA 2026 Daily Practice Quiz}}\\[0.3cm]
    {\large """ + datetime.now().strftime("%B %d, %Y") + r"""}\\[0.2cm]
    \textit{Solve all questions before checking answers!}
\end{center}

\vspace{1cm}

"""
    
    # Add questions
    for i, (subject, topic, question) in enumerate(questions, 1):
        latex_content += f"\n\\section*{{Question {i}: {subject}}}\n"
        latex_content += f"\\textbf{{Topic:}} {topic}\\\\[0.3cm]\n\n"
        latex_content += question + "\n\n"
        latex_content += "\\vspace{0.5cm}\n\\hrule\n\\vspace{0.5cm}\n\n"
    
    # Add answers section
    latex_content += r"""
\newpage
\section*{\textcolor{red}{ANSWERS}}
\textit{Check only after solving all questions!}

\vspace{1cm}

"""
    
    for i, (subject, topic, question) in enumerate(questions, 1):
        # Extract answer
        if "Answer:" in question:
            answer_lines = [line for line in question.split('\n') if line.strip().startswith('Answer:')]
            if answer_lines:
                latex_content += f"\\textbf{{{i}. {subject}:}} {answer_lines[0]}\\\\\n\n"
    
    latex_content += r"\end{document}"
    return latex_content


def compile_latex_to_pdf(latex_content, output_name="daily_quiz"):
    """Compile LaTeX to PDF using pdflatex"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, f"{output_name}.tex")
        
        # Write LaTeX file
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"📄 LaTeX file created")
        
        try:
            # Compile with pdflatex (run twice for references)
            for run in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', f'{output_name}.tex'],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            
            if result.returncode == 0:
                # Copy PDF to current directory
                pdf_src = os.path.join(tmpdir, f"{output_name}.pdf")
                pdf_dst = f"{output_name}.pdf"
                
                with open(pdf_src, 'rb') as src, open(pdf_dst, 'wb') as dst:
                    dst.write(src.read())
                
                print(f"✅ PDF created successfully!")
                return pdf_dst
            else:
                print(f"❌ pdflatex compilation failed!")
                print(f"Error: {result.stderr[:500]}")
                return None
                
        except Exception as e:
            print(f"❌ Error compiling PDF: {e}")
            return None

# ============================================================================
# EMAIL DELIVERY
# ============================================================================

def send_email(pdf_file, questions):
    """Send quiz email via Gmail"""
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    msg['Subject'] = f"Daily GATE DA Quiz - {datetime.now().strftime('%b %d, %Y')} [LaTeX Edition]"
    
    # Email body
    topics_list = '\n'.join([f"  • {subj}: {topic}" for subj, topic, _ in questions])
    
    body = f"""Hello GATE DA 2026 Warrior!

Your daily quiz with PROFESSIONAL LaTeX formatting is ready! 📚✨

Today's Topics:
{topics_list}

✨ NEW: Questions now feature beautiful mathematical notation!
- Proper fractions, matrices, Greek letters
- Publication-quality formatting
- Just like your textbooks!

💡 Tips:
- Solve all questions before checking answers
- Focus on understanding the concepts
- Practice similar variations

Good luck and happy learning!

---
Powered by FREE AI (Groq + LaTeX + GitHub Actions)
Keep grinding! GATE DA 2026 is yours! 🎓
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
    
    # Prepare recipient list
    recipients = [GMAIL_USER] + [email.strip() for email in FRIENDS if email.strip()]
    
    # Send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg, to_addrs=recipients)
        
        print(f"✅ Email sent to {len(recipients)} recipient(s)!")
    
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("DAILY GATE DA QUIZ GENERATOR - LaTeX Edition")
    print("="*60 + "\n")
    
    # Collect topics for today
    topic_list = []
    
    print("📋 Selecting today's topics...\n")
    
    for subject, topics in SYLLABUS.items():
        # Get current topic index
        topic_index = progress[subject] % len(topics)
        topic = topics[topic_index]
        topic_list.append((subject, topic))
        print(f"  • {subject}: {topic}")
        
        # Update progress for next day
        progress[subject] = topic_index + 1
    
    print(f"\n🤖 Generating all {len(topic_list)} questions in ONE API call...\n")
    
    # Generate all questions at once - MUCH BETTER!
    questions = generate_all_questions_latex(topic_list)
    
    if not questions:
        print("❌ Failed to generate questions! Check API key and connection.")
        return
    
    print(f"✅ Generated {len(questions)} questions!\n")
    
    # Create LaTeX document
    print("📄 Creating LaTeX document...")
    latex_doc = create_latex_document(questions)
    
    # Compile to PDF
    print("📊 Compiling to PDF with LaTeX...")
    pdf_file = compile_latex_to_pdf(latex_doc)
    
    if not pdf_file:
        print("❌ PDF compilation failed! Cannot send email.")
        return
    
    # Send email
    print("📧 Sending email...")
    send_email(pdf_file, questions)
    
    # Save progress
    with open('progress.json', 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)
    
    print("\n" + "="*60)
    print("SUCCESS! ✅")
    print("="*60 + "\n")
    print(f"📧 Quiz emailed with beautiful LaTeX formatting!")
    print(f"📊 Topics covered:")
    for subject, topic, _ in questions:
        print(f"  - {subject}: {topic}")
    print("\n💡 One API call = More efficient + Lower cost!")
    print("\nKeep grinding! GATE DA 2026 is yours! 🎓\n")

if __name__ == "__main__":
    main()
