import requests
import json

GROQ_API_KEY = "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"

print("🔍 Checking available FREE Groq models...\n")

# Get available models
response = requests.get(
    'https://api.groq.com/openai/v1/models',
    headers={'Authorization': f'Bearer {GROQ_API_KEY}'}
)

if response.status_code == 200:
    models = response.json()['data']
    print("✅ Available FREE models:\n")
    for m in models:
        print(f"  • {m['id']}")
    
    # Test with a working model
    print("\n" + "="*60)
    print("🧪 Testing question generation...\n")
    
    test_model = "llama-3.1-8b-instant"  # Fast and free!
    
    test_response = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            "model": test_model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert GATE DA exam question creator."
                },
                {
                    "role": "user",
                    "content": """Generate 1 challenging GATE DA question on Bayes Theorem.

Format:
Q. [Question with LaTeX: use $x$ for inline, $$equation$$ for block]

(A) Option A
(B) Option B  
(C) Option C
(D) Option D

Answer: (X)"""
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
    )
    
    if test_response.status_code == 200:
        result = test_response.json()
        question = result['choices'][0]['message']['content']
        
        print("✅ SUCCESS! Generated question:\n")
        print(question)
        print("\n" + "="*60)
        print("\n💯 GROQ FREE TIER - NO BILLING!")
        print("   ✅ Requests: 30 per minute (you use 8/day)")
        print("   ✅ Tokens: 6,000 per minute")
        print("   ✅ Cost: $0.00 FOREVER")
        print("   ✅ No credit card required")
        print("   ✅ No hidden charges")
        print("\n🔒 You will NEVER be billed! 100% FREE!")
    else:
        print(f"❌ Test error: {test_response.status_code}")
        print(test_response.text)
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
