# 🎓 Daily GATE DA Quiz Mailer

**Automated daily GATE Data Science & AI quiz delivery via email using AI-generated questions.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Free](https://img.shields.io/badge/Cost-$0-brightgreen.svg)](https://github.com/ManojSwagath/daily-gate-quiz-mailer)

## Overview

Automatically generates and emails 8 challenging GATE DA questions daily to you and your study group. Questions cover all 94 topics across 8 core subjects with proper LaTeX formatting.

## Features

- 🤖 **AI-Powered**: Uses Groq API (LLaMA 3.3 70B) for question generation
- 📧 **Auto Delivery**: Gmail SMTP sends PDF to multiple recipients daily
- 🔄 **Smart Rotation**: Cycles through all syllabus topics systematically
- 📊 **PDF Format**: Professional formatting with questions and answers
- ⏰ **Scheduled**: Runs daily at 6:00 AM IST via GitHub Actions
- 💯 **100% Free**: No subscriptions, no cloud costs

## Tech Stack

- **AI**: Groq API (free tier)
- **Automation**: GitHub Actions (free tier)
- **Email**: Gmail SMTP
- **PDF**: FPDF2 library
- **Language**: Python 3.11+

## Quick Setup

### 1. Fork This Repository

Click "Fork" at the top right of this page.

### 2. Add GitHub Secrets

Go to: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Add these 4 secrets:

| Name | Value | How to Get |
|------|-------|------------|
| `GROQ_API_KEY` | Your Groq API key | [Get from Groq Console](https://console.groq.com/keys) |
| `GMAIL_USER` | your.email@gmail.com | Your Gmail address |
| `GMAIL_PASS` | xxxx xxxx xxxx xxxx | [Gmail App Password](https://myaccount.google.com/apppasswords) |
| `FRIENDS` | email1@gmail.com,email2@gmail.com | Comma-separated recipient list |

### 3. Enable GitHub Actions

1. Go to `Actions` tab
2. Click "I understand my workflows, go ahead and enable them"

### 4. Test Run (Optional)

1. Go to `Actions` → `Daily DA 2026 Quiz Mailer`
2. Click `Run workflow` → `Run workflow`
3. Check your email in 2-3 minutes

## Configuration

### Change Schedule

Edit `.github/workflows/daily.yml`:
```yaml
schedule:
  - cron: '30 0 * * *'  # 6:00 AM IST (default)
```

### Modify Syllabus

Edit `syllabus.json` to add/remove topics.

### Add More Recipients

Update `FRIENDS` secret with comma-separated emails (no spaces).

## Project Structure

```
daily-gate-quiz-mailer/
├── .github/
│   └── workflows/
│       └── daily.yml           # GitHub Actions workflow (scheduled automation)
├── generate_quiz.py            # Main quiz generation script
├── syllabus.json              # GATE DA 2026 complete syllabus (94 topics)
├── progress.json              # Auto-updated topic tracker
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
├── LICENSE                    # MIT License
└── .gitignore                # Git ignore rules
```

## GATE DA Syllabus Coverage

**94 Topics across 8 Subjects:**

1. Probability and Statistics (17 topics)
2. Linear Algebra (13 topics)
3. Calculus and Optimization (6 topics)
4. Programming and Data Structures (11 topics)
5. Database Management and Warehousing (16 topics)
6. Machine Learning - Supervised (14 topics)
7. Machine Learning - Unsupervised (8 topics)
8. Artificial Intelligence (9 topics)

## How It Works

```
Daily Trigger (6 AM IST)
    ↓
Select 8 Topics (1 per subject)
    ↓
Groq API Generates Questions
    ↓
Create PDF with FPDF2
    ↓
Send via Gmail SMTP
    ↓
Update Progress Tracker
```

## Troubleshooting

**Email not received?**
- Check GitHub Actions logs in `Actions` tab
- Verify all 4 secrets are added correctly
- Check spam/junk folder

**Workflow not running?**
- Ensure GitHub Actions is enabled
- Check if workflow is disabled in `Actions` tab
- Verify cron schedule syntax

**Questions quality issues?**
- Groq API free tier has rate limits (30 req/min)
- Check API key validity at [Groq Console](https://console.groq.com/)

## Contributing

Pull requests welcome! For major changes, please open an issue first.

## License

[MIT](LICENSE)

## Acknowledgments

- Groq for free AI API
- GitHub for free CI/CD
- GATE DA 2026 syllabus

---

**⭐ Star this repo if it helps your GATE prep!**
