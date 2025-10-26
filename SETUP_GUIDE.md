# 🚀 COMPLETE SETUP GUIDE - Groq Edition

## Why We Switched to Groq

❌ **Hugging Face Issues:**
- API down until Nov 1st
- Slow inference (20+ seconds)
- Model loading delays

✅ **Groq Benefits:**
- ⚡ 100x FASTER (2-3 seconds!)
- ✅ Always available (99.9% uptime)
- 🎯 Better questions (LLaMA 3.1 70B)
- 💯 Still 100% FREE!

---

## Step 1: Get Groq API Key (30 seconds)

### Create Account:
1. Visit: **https://console.groq.com/keys**
2. Click **"Sign in with GitHub"** (or Google)
3. Authorize Groq

### Generate Key:
1. Click **"Create API Key"**
2. Name: `daily-gate-quiz`
3. Click **"Submit"**
4. **COPY THE KEY** - looks like: `gsk_abcd1234efgh5678...`

⚠️ **CRITICAL**: Save it somewhere safe! You can't see it again!

---

## Step 2: Get Gmail App Password (2 minutes)

### Prerequisites:
- Gmail account
- 2-Step Verification enabled

### Steps:
1. **Enable 2-Step Verification** (if not already):
   - Visit: https://myaccount.google.com/security
   - Scroll to "2-Step Verification" → Turn it ON
   - Follow the prompts

2. **Generate App Password**:
   - Visit: https://myaccount.google.com/apppasswords
   - Select app: **"Mail"**
   - Select device: **"Other (Custom name)"**
   - Type: `GATE Quiz Mailer`
   - Click **"Generate"**
   - **COPY THE 16-CHARACTER PASSWORD** (no spaces)
     - Example: `abcd efgh ijkl mnop`

---

## Step 3: Add GitHub Secrets (2 minutes)

### Go to Your Repo Settings:
URL: `https://github.com/YOUR_USERNAME/daily-gate-quiz-mailer/settings/secrets/actions`

### Add 4 Secrets:

Click **"New repository secret"** 4 times and add these:

#### Secret 1: GROQ_API_KEY
- **Name**: `GROQ_API_KEY`
- **Value**: `gsk_...your...key...here...` (from Step 1)
- Click "Add secret"

#### Secret 2: GMAIL_USER
- **Name**: `GMAIL_USER`
- **Value**: `your.email@gmail.com`
- Click "Add secret"

#### Secret 3: GMAIL_PASS
- **Name**: `GMAIL_PASS`
- **Value**: `abcd efgh ijkl mnop` (16 chars from Step 2)
- Click "Add secret"

#### Secret 4: FRIENDS
- **Name**: `FRIENDS`
- **Value**: `friend1@gmail.com,friend2@gmail.com,friend3@gmail.com`
- Click "Add secret"

⚠️ **Format for FRIENDS**: Comma-separated, NO SPACES!

---

## Step 4: Push Updated Code (1 minute)

### In PowerShell:

```powershell
cd e:\Mail
git add .
git commit -m "Switch to Groq API - faster and more reliable!"
git push
```

---

## Step 5: Test the Workflow (2 minutes)

### Manual Test Run:

1. **Go to Actions Tab**:
   - URL: `https://github.com/YOUR_USERNAME/daily-gate-quiz-mailer/actions`

2. **Run Workflow**:
   - Click "Daily DA 2026 Quiz Mailer" (left sidebar)
   - Click "Run workflow" button (right side)
   - Select branch: `main`
   - Click green "Run workflow" button

3. **Monitor Progress**:
   - Refresh page after 10 seconds
   - Click on the running workflow (yellow dot)
   - Click "Generate and send quiz" to see logs
   - Wait 2-3 minutes

4. **Check Your Email**:
   - Open your Gmail inbox
   - Look for "Daily DA 2026 Quiz - [Date]"
   - Download the PDF attachment
   - Verify 8 questions are generated correctly

---

## ✅ Success Checklist

After testing, you should see:

- [ ] Workflow completed successfully (green checkmark)
- [ ] Email received in inbox (check spam if not)
- [ ] PDF attachment opens correctly
- [ ] 8 questions with proper formatting
- [ ] Answers section at bottom
- [ ] Friends also received email

---

## 🔧 What Happens Next?

### Automatic Daily Runs:
- **Time**: Every day at 6:00 AM IST
- **Process**:
  1. GitHub Actions wakes up
  2. Calls Groq API to generate 8 questions
  3. Creates PDF with FPDF2
  4. Sends email to you + friends
  5. Updates progress.json for next day

### Topic Rotation:
- Each subject gets 1 question daily
- System cycles through all 94 topics
- Complete coverage in ~12 days
- Then repeats with fresh questions!

---

## 🐛 Troubleshooting

### ❌ "Error: Missing environment variables"
**Fix**: Double-check all 4 secrets are added correctly
- Names must be EXACT: `GROQ_API_KEY`, `GMAIL_USER`, `GMAIL_PASS`, `FRIENDS`
- No extra spaces in values

### ❌ "Groq API error: 401 Unauthorized"
**Fix**: Wrong API key
- Go back to https://console.groq.com/keys
- Create a NEW key
- Update `GROQ_API_KEY` secret

### ❌ "SMTP authentication failed"
**Fix**: Wrong Gmail App Password
- Generate NEW app password: https://myaccount.google.com/apppasswords
- Update `GMAIL_PASS` secret with NEW 16-char password
- Make sure 2-Step Verification is ON

### ❌ Email not received
**Check**:
1. Spam/Junk folder
2. GitHub Actions logs for errors
3. Gmail "Blocked" senders
4. `GMAIL_USER` email is correct

### ❌ Workflow doesn't run automatically
**Fix**:
1. Settings → Actions → General
2. "Allow all actions and reusable workflows"
3. Enable "Read and write permissions"
4. Save

---

## 📊 Free Tier Limits

### Groq (More than enough!):
```
✅ Requests: 30 per minute
✅ Tokens: 6,000 per minute
✅ Daily usage: Unlimited

Your usage: 8 requests/day = 0.4% of limit 😎
```

### GitHub Actions:
```
✅ Minutes: 2,000 per month (free tier)
✅ Storage: Unlimited for code

Your usage: ~30 min/month = 1.5% of limit 🎉
```

### Gmail:
```
✅ Emails: 500 per day (normal accounts)

Your usage: 1 email/day = 0.2% of limit 🚀
```

**You're nowhere close to any limits!** 💯

---

## 🎯 Next Steps

1. ✅ Verify test email received
2. ✅ Check PDF opens correctly
3. ✅ Wait for tomorrow's automatic email (6 AM IST)
4. ✅ Share repo with your 3 friends!

---

## 📚 Additional Resources

- [GROQ_SETUP.md](GROQ_SETUP.md) - Detailed Groq key setup
- [IMPORTANT_TOPICS.md](IMPORTANT_TOPICS.md) - GATE DA topic priorities
- [README.md](README.md) - Full project documentation

---

**Need help?** Open an issue on GitHub!

🎉 **Congrats! You're now getting daily GATE DA quizzes for FREE!** 🎉
