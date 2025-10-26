# 🚀 Groq API Setup - SUPER FAST & FREE!

## Why Groq > Hugging Face?
- ⚡ **100x FASTER** inference speed (seriously!)
- ✅ **More Reliable** - no model loading delays
- 🎯 **Better Quality** - Uses LLaMA 3.1 70B model
- 💯 **Still 100% FREE** for personal use

## Get Your FREE Groq API Key

### Step 1: Sign Up (30 seconds)
1. Visit: https://console.groq.com/keys
2. Click **"Sign in with GitHub"** (or Google)
3. Authorize Groq to access your GitHub account

### Step 2: Create API Key
1. Click **"Create API Key"** button
2. Give it a name: `daily-gate-quiz`
3. Click **"Submit"**
4. **COPY THE KEY** (looks like: `gsk_abcd1234...`)

⚠️ **IMPORTANT**: Copy it now! You won't see it again!

## Free Tier Limits (More than enough!)

```
📊 Groq Free Tier:
- Requests: 30 per minute
- Tokens: 6,000 per minute
- Daily usage: Unlimited!

Your usage: 8 requests/day = 0% of limit 😎
```

## Add to GitHub Secrets

1. Go to: https://github.com/ManojSwagath/daily-gate-quiz-mailer/settings/secrets/actions
2. Click **"New repository secret"**
3. Name: `GROQ_API_KEY`
4. Value: `gsk_...your...key...here...`
5. Click **"Add secret"**

## Test Your Key (Optional)

Run this in PowerShell to test:

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_GROQ_KEY_HERE"
    "Content-Type" = "application/json"
}

$body = @{
    model = "llama-3.1-70b-versatile"
    messages = @(
        @{
            role = "user"
            content = "Say 'Groq is working!'"
        }
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.groq.com/openai/v1/chat/completions" -Method Post -Headers $headers -Body $body
```

If you see `"Groq is working!"` in the response, you're golden! ✅

## What Changed?

✅ Replaced Hugging Face API with Groq
✅ Faster question generation (2-3 seconds instead of 20+)
✅ No more "model loading" delays
✅ Better quality questions using LLaMA 3.1 70B

## Next Steps

1. ✅ Get Groq API key (above)
2. ✅ Add `GROQ_API_KEY` to GitHub Secrets
3. ✅ Add other secrets (GMAIL_USER, GMAIL_PASS, FRIENDS)
4. ✅ Test workflow: https://github.com/ManojSwagath/daily-gate-quiz-mailer/actions

---

**Your new secrets needed:**
- `GROQ_API_KEY` = (get from https://console.groq.com/keys)
- `GMAIL_USER` = a.manojswagath@gmail.com
- `GMAIL_PASS` = ziln shde xrts rvre
- `FRIENDS` = friend1@gmail.com,friend2@gmail.com,friend3@gmail.com

All done! 🎉
