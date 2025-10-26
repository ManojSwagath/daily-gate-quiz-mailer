#!/usr/bin/env python3
"""
Simple demo: How topic rotation works daily
Shows you exactly which topics will be picked each day
"""

import json

# Load your syllabus
with open('syllabus.json', 'r', encoding='utf-8') as f:
    SYLLABUS = json.load(f)

# Simulate progress (starts at 0 for each subject)
progress = {subject: 0 for subject in SYLLABUS.keys()}

print("="*70)
print("DAILY TOPIC ROTATION DEMO - Next 15 Days")
print("="*70)
print("\nThis shows which topics will be picked each day.\n")

# Simulate 15 days
for day in range(1, 16):
    print(f"\n📅 DAY {day}:")
    print("-" * 70)
    
    daily_topics = []
    
    # Pick one topic from each subject (8 subjects = 8 questions/day)
    for subject, topics in SYLLABUS.items():
        # Get current topic index (cycles through topics)
        topic_index = progress[subject] % len(topics)
        topic = topics[topic_index]
        
        daily_topics.append(f"  {subject:35} → {topic}")
        
        # Move to next topic for tomorrow
        progress[subject] = topic_index + 1
    
    # Print today's topics
    for t in daily_topics:
        print(t)

print("\n" + "="*70)
print("✅ After all topics are covered, it cycles back to the beginning!")
print("="*70)

# Show completion percentage
print(f"\n📊 Total Topics: {sum(len(topics) for topics in SYLLABUS.values())} topics")
print(f"📊 Days to cover all: ~{max(len(topics) for topics in SYLLABUS.values())} days")
print(f"📊 Questions per day: {len(SYLLABUS)} (1 per subject)")
