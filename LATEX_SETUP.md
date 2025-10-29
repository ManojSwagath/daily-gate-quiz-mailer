# 🎓 LaTeX Edition Setup Guide

## ✨ What's New?

Your quiz mailer now generates **professional LaTeX-formatted PDFs** with:
- ✅ Beautiful mathematical notation (fractions, matrices, integrals)
- ✅ Greek letters and special symbols
- ✅ Publication-quality formatting
- ✅ Looks like a real textbook!
- ✅ **ONE API call** - More efficient, lower cost!

---

## � Key Improvement: Single API Call

Instead of making 8 separate API calls (one per question), the new approach:
- 📞 Makes **ONE API call** to generate all 8 questions at once
- 💰 **More cost-effective** - Uses fewer tokens
- ⚡ **Faster** - No delays between questions
- 🎯 **Better consistency** - All questions in same style

---

## 🔧 Setup Instructions

### Step 1: No Additional Secrets Needed!

You only need the **existing secrets**:
- ✅ `GROQ_API_KEY` (your existing key)
- ✅ `GMAIL_USER`
- ✅ `GMAIL_PASS`
- ✅ `FRIENDS` (optional)

**No second API key required!** 🎉

Two options:

### Step 2: Enable the LaTeX Workflow

Two options:

**Option A: Replace the old workflow (Recommended)**
```bash
cd "d:\projects\Like oyu\daily-gate-quiz-mailer"
Remove-Item .github/workflows/daily.yml
Rename-Item .github/workflows/daily_latex.yml daily.yml
```

**Option B: Run both workflows**
- Keep both `daily.yml` (old) and `daily_latex.yml` (new)
- Old: Plain Unicode PDFs
- New: Beautiful LaTeX PDFs

### Step 3: Test It!

1. Go to: `https://github.com/ManojSwagath/daily-gate-quiz-mailer/actions`
2. Click **Daily GATE Quiz Mailer (LaTeX Edition)**
3. Click **Run workflow** → **Run workflow**
4. Wait 3-5 minutes
5. **Check your email for the beautiful PDF!** 📧✨

---

## 📊 How It Works

```
GitHub Actions (Ubuntu)
    ↓
Install LaTeX (pdflatex)
    ↓
Generate 8 questions with LaTeX notation (Groq API)
    ↓
Create .tex file
    ↓
Compile to PDF (pdflatex)
    ↓
Email PDF to you + friends
    ↓
Update progress.json
```

---

## 🔑 Required Secrets

Make sure you have these secrets set:

| Secret Name | Description | Required |
|------------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |
| `GMAIL_USER` | Your Gmail address | ✅ Yes |
| `GMAIL_PASS` | Gmail app password | ✅ Yes |
| `FRIENDS` | Comma-separated emails | ⚪ Optional |

**Note:** No second API key needed! Uses only ONE API call. 🎯

---

## 📝 Files Overview

### New Files:
- `generate_quiz_latex.py` - Main script with LaTeX support
- `.github/workflows/daily_latex.yml` - Workflow with LaTeX installation
- `LATEX_SETUP.md` - This file

### Test Files:
- `test_latex_generation.py` - Local test script
- `test_quiz.tex` - Sample LaTeX output

---

## 🎨 LaTeX vs Unicode Comparison

### Before (Unicode):
```
x² + σ² ≤ μ
P(X ≤ x) = ∫ f(t)dt
```
- Limited symbols
- Basic formatting

### After (LaTeX):
```latex
$x^2 + \sigma^2 \leq \mu$
$P(X \leq x) = \int_{-\infty}^{x} f(t)dt$
```
- Professional notation
- Publication quality
- **Beautiful!** ✨

---

## 🚀 Benefits

1. **Professional Quality**: PDFs look like textbook pages
2. **Better Learning**: Proper math notation aids understanding
3. **Impressive**: Share with friends and teachers
4. **Free**: Still 100% free (GitHub Actions + Groq API)
5. **Automatic**: Runs daily at 6 AM IST
6. **Efficient**: ONE API call instead of 8 - saves tokens! 💰

---

## 🐛 Troubleshooting

### Workflow fails at "Install LaTeX"
- This is rare; LaTeX installation is automatic on Ubuntu
- Check GitHub Actions logs

### PDF not generated
- Check that `GROQ_LATEX_API_KEY` is set correctly
- Verify API key has remaining credits at https://console.groq.com

### Questions not in LaTeX format
- AI might occasionally skip LaTeX formatting
- Re-run the workflow for better results

---

## 📧 What You'll Receive

**Email Subject:** Daily GATE DA Quiz - [Date] [LaTeX Edition]

**Email Body:** 
- List of topics covered
- Mention of LaTeX formatting
- Motivational message

**Attachment:** Beautiful PDF with:
- Professional formatting
- 8 questions with LaTeX math
- Answers section at the end

---

## 🎓 Ready to Deploy?

Once you've added the `GROQ_LATEX_API_KEY` secret and pushed the files:

1. Commit and push:
```bash
git add .
git commit -m "feat: Add LaTeX PDF generation with beautiful math notation"
git push
```

2. Test manually in GitHub Actions

3. Enjoy your daily professional quiz PDFs! 🎉

---

**Questions?** The LaTeX edition is fully compatible with the original - you can always switch back!

**Love it?** Star the repo and share with your study group! ⭐
