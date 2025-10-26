#!/usr/bin/env python3
"""Remove duplicate PDF code"""

with open('generate_quiz.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove lines 303-413 (duplicate FPDF code)
new_lines = lines[:302] + lines[413:]

with open('generate_quiz.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Removed duplicate code (lines 303-413)")
print(f"New file has {len(new_lines)} lines (was {len(lines)})")
