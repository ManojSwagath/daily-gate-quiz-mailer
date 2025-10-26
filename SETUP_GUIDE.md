# 🚀 SETUP INSTRUCTIONS - Follow These Steps!

## ✅ What's Already Built

I've created all the files you need:
- ✅ `generate_quiz.py` - Main script (AI + PDF + Email)
- ✅ `syllabus.json` - GATE topics (customize if you want!)
- ✅ `requirements.txt` - Python packages
- ✅ `.github/workflows/daily.yml` - Auto-runs daily at 6 AM IST
- ✅ `.env.example` - Template for secrets
- ✅ `README.md` - Full documentation

---

## 📋 NOW DO THESE STEPS (15 Minutes Total)

### STEP 1: Create GitHub Account & Repository (3 minutes)

1. **Go to**: https://github.com/signup
   - Create account if you don't have one (FREE!)

2. **Create new repository**:
   - Click the `+` icon (top right) → "New repository"
   - Name: `gate-quiz-mailer` (or any name you like)
   - Description: "Daily GATE quiz automation"
   - Choose: **Public** or **Private** (both are FREE!)
   - ✅ Check "Add a README file"
   - Click "Create repository"

3. **Upload all files**:
   - Click "Add file" → "Upload files"
   - Drag and drop ALL files from `e:\Mail\` folder:
     - `generate_quiz.py`
     - `syllabus.json`
     - `requirements.txt`
     - `.github/workflows/daily.yml` (create folder structure)
     - `.gitignore`
     - `README.md`
   - Click "Commit changes"

---

### STEP 2: Get Hugging Face API Token (2 minutes)

1. **Go to**: https://huggingface.co/join
   - Sign up with email (FREE!)

2. **Create API Token**:
   - Click your profile picture (top right) → "Settings"
   - Click "Access Tokens" (left menu)
   - Click "New token"
   - Name: `gate-quiz`
   - Type: Select "Read"
   - Click "Generate token"
   - **COPY THE TOKEN** (starts with `hf_...`)
   - ⚠️ Save it somewhere - you'll need it in Step 4!

---

### STEP 3: Setup Gmail App Password (5 minutes)

1. **Enable 2-Step Verification**:
   - Go to: https://myaccount.google.com/security
   - Scroll to "How you sign in to Google"
   - Click "2-Step Verification" → Turn it ON
   - Follow the prompts (use phone number)

2. **Create App Password**:
   - After 2FA is enabled, go back to: https://myaccount.google.com/security
   - Scroll to "2-Step Verification" → Click it
   - Scroll down to "App passwords" → Click it
   - Select app: "Mail"
   - Select device: "Other (Custom name)" → Type: "GATE Quiz"
   - Click "Generate"
   - **COPY THE 16-CHARACTER PASSWORD** (looks like: `abcd efgh ijkl mnop`)
   - ⚠️ Save it - you'll need it in Step 4!

---

### STEP 4: Add Secrets to GitHub (3 minutes)

1. **Go to your GitHub repository**
   - Click "Settings" tab (top menu)
   - Click "Secrets and variables" → "Actions" (left menu)
   - Click "New repository secret" button

2. **Add 4 secrets** (one by one):

   **Secret 1:**
   - Name: `HF_TOKEN`
   - Value: Your Hugging Face token from Step 2 (starts with `hf_...`)
   - Click "Add secret"

   **Secret 2:**
   - Name: `GMAIL_USER`
   - Value: Your Gmail address (e.g., `yourname@gmail.com`)
   - Click "Add secret"

   **Secret 3:**
   - Name: `GMAIL_PASS`
   - Value: Your Gmail App Password from Step 3 (16 chars: `abcd efgh ijkl mnop`)
   - Click "Add secret"

   **Secret 4:**
   - Name: `FRIENDS`
   - Value: Your friends' emails, comma-separated
   - Example: `friend1@gmail.com,friend2@gmail.com,friend3@gmail.com`
   - Click "Add secret"

---

### STEP 5: Test It Manually! (2 minutes)

1. **Go to "Actions" tab** in your GitHub repo
2. Click "Daily GATE Quiz Mailer" (left side)
3. Click "Run workflow" button (right side)
4. Click the green "Run workflow" button in the popup
5. **Wait 1-2 minutes**
6. Click on the running workflow to see logs
7. **Check your email!** 📧🎉

---

## 🎉 YOU'RE DONE!

### What Happens Now?

✅ **Every day at 6:00 AM IST**, GitHub will automatically:
1. Generate 5 AI-powered GATE questions
2. Create a beautiful PDF
3. Email it to you + your 3 friends
4. Update progress to next topics

### ⚠️ Important Notes

- **First run might take 30 seconds** (Hugging Face model loads)
- **Check spam folder** if you don't see email
- **It's 100% FREE forever!** No credit card needed

---

## 🔧 Optional: Customize

### Change Quiz Time
Edit `.github/workflows/daily.yml`:
```yaml
- cron: '30 0 * * *'  # 6:00 AM IST (00:30 UTC)
```

Use https://crontab.guru to find your preferred time!

**Popular times:**
- `0 0 * * *` - 5:30 AM IST
- `0 12 * * *` - 5:30 PM IST
- `30 13 * * *` - 7:00 PM IST

### Add More Subjects
Edit `syllabus.json` and add your topics!

### Add More Friends
Go to GitHub repo → Settings → Secrets → Edit `FRIENDS`

---

## 🆘 Troubleshooting

### No email received?
1. ✅ Check spam/junk folder
2. ✅ Verify all 4 GitHub Secrets are correct
3. ✅ Check Actions tab for error logs
4. ✅ Make sure Gmail App Password is correct (no spaces!)

### "Authentication failed" error?
- Regenerate Gmail App Password (Step 3)
- Update `GMAIL_PASS` secret in GitHub

### Questions look weird?
- Hugging Face model might be loading
- Run workflow again after 5 minutes
- Free tier models take 20-30 seconds to warm up

---

## 📞 Need Help?

- Read `README.md` for detailed documentation
- Check GitHub Actions logs for error messages
- Verify all secrets are set correctly

---

## 🎓 GOOD LUCK WITH GATE 2026! 🔥

You're all set! Tomorrow morning at 6 AM, you'll get your first automated quiz!

**Keep grinding! 💪**
