#!/usr/bin/env python3
"""
FINAL TEST - Generate full 8-question quiz before GitHub deployment
"""

import os
os.environ['GROQ_API_KEY'] = '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'
os.environ['GMAIL_USER'] = 'a.manojswagath@gmail.com'
os.environ['GMAIL_PASS'] = 'ziln shde xrts rvre'
os.environ['FRIENDS'] = ''  # No friends for testing

print("\n" + "="*70)
print("FINAL TEST - Full 8-Question Quiz")
print("="*70)
print("\nThis will:")
print("  1. Generate 8 GATE DA questions (natural language)")
print("  2. Create PDF with proper formatting")
print("  3. Send email to you")
print("  4. Open PDF automatically")
print("\nIf this looks good → GitHub workflow is READY!")
print("="*70)
input("\nPress ENTER to start test...")

import generate_quiz
generate_quiz.main()

print("\n" + "="*70)
print("TEST COMPLETE!")
print("="*70)
print("\n📧 Check your email: a.manojswagath@gmail.com")
print("📄 Check the PDF that opened")
print("\nIf both look good:")
print("  ✅ Questions are readable and natural")
print("  ✅ PDF formatting is clean")
print("  ✅ Email received successfully")
print("\nThen:")
print("  → Go to GitHub Actions")
print("  → Enable workflows")
print("  → Run manual test")
print("  → Daily emails at 6 AM IST will start!")
print("\n" + "="*70)
