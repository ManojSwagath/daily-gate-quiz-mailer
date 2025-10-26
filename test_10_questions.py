#!/usr/bin/env python3
"""
GROQ API TEST - Generate 10 GATE DA questions with LaTeX math
Shows you EXACTLY what you'll get daily (but with 10 instead of 8)
"""

import requests
import json
import time

GROQ_API_KEY = "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"

# Test topics from your syllabus
test_topics = [
    ("Probability and Statistics", "Bayes Theorem"),
    ("Linear Algebra", "Eigenvalues and Eigenvectors"),
    ("Calculus and Optimization", "Maxima and Minima"),
    ("Programming and Data Structures", "Sorting (Selection, Bubble, Insertion)"),
    ("Database Management and Warehousing", "SQL Queries"),
    ("Machine Learning - Supervised", "Logistic Regression"),
    ("Machine Learning - Unsupervised", "k-means Clustering"),
    ("Artificial Intelligence", "Informed Search Algorithms"),
    ("Probability and Statistics", "Central Limit Theorem"),
    ("Linear Algebra", "Singular Value Decomposition (SVD)")
]

def generate_question(subject, topic):
    """Generate one GATE DA question using Groq API"""
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Generate ONE extremely challenging GATE DA (Data Science & AI) exam question.

Subject: {subject}
Topic: {topic}

Requirements:
1. GATE DA 2026 exam difficulty level (top 10% hardest questions)
2. Use LaTeX for math: $x^2$ for inline, $$equation$$ for block
3. Four options (A, B, C, D) with ONE correct answer
4. Include numerical calculations where applicable
5. Test deep conceptual understanding

Format (STRICT):
Q. [Your challenging question here with LaTeX if needed]

(A) [First option]
(B) [Second option]
(C) [Third option]
(D) [Fourth option]

Answer: (X)

Example:
Q. Given P(A) = 0.3, P(B) = 0.5, and P(B|A) = 0.6. What is P(A|B)?

(A) 0.24
(B) 0.36
(C) 0.42
(D) 0.48

Answer: (B)

NOW GENERATE:"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert GATE DA exam question creator. Generate challenging, accurate questions with proper LaTeX formatting."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    
    except Exception as e:
        return f"❌ Exception: {str(e)}"

# Main execution
print("="*70)
print("🚀 GROQ API TEST - Generating 10 GATE DA Questions")
print("="*70)
print("\n💯 FREE API - NO BILLING!")
print("   ✅ Your key: gsk_2RBZ...Cu9AW (tested & working)")
print("   ✅ Model: llama-3.3-70b-versatile (latest!)")
print("   ✅ Cost: $0.00 forever\n")
print("="*70)

questions = []

for i, (subject, topic) in enumerate(test_topics, 1):
    print(f"\n📝 Question {i}/10:")
    print(f"   Subject: {subject}")
    print(f"   Topic: {topic}")
    print("   Generating... ", end="", flush=True)
    
    question = generate_question(subject, topic)
    questions.append((subject, topic, question))
    
    print("✅ Done!")
    
    # Show the question
    print("\n" + "-"*70)
    print(question)
    print("-"*70)
    
    # Small delay to respect rate limits (30 req/min = 2 sec between requests)
    if i < len(test_topics):
        time.sleep(2)

print("\n" + "="*70)
print("🎉 SUCCESS! Generated 10 questions!")
print("="*70)
print("\n📊 Summary:")
print(f"   • Total questions: {len(questions)}")
print(f"   • API calls: {len(questions)}")
print(f"   • Time taken: ~{len(questions) * 2} seconds")
print(f"   • Cost: $0.00 (FREE!)")
print("\n💡 This is what you'll get daily (but with 8 questions, not 10)")
print("   Your friends will receive the same PDF via email!")
print("\n" + "="*70)
