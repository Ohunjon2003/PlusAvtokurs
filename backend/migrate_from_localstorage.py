#!/usr/bin/env python
"""
Migration script to import data from localStorage JSON exports to Django database
Usage: python migrate_from_localstorage.py --file data.json
"""

import json
import os
import django
from datetime import datetime
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import (
    Category, Question, TestResult, CustomUser, CustomUserProfile,
    ActivityLog, ChatMessage, UserGoal, Bookmark, StudyMaterial, Notification
)

def migrate_categories(data):
    """Migrate categories"""
    if 'pa_categories' not in data:
        print("❌ No categories found")
        return
    
    categories = data['pa_categories']
    for cat in categories:
        Category.objects.get_or_create(
            id=cat['id'],
            defaults={
                'nameUz': cat.get('nameUz', 'Unknown'),
                'emoji': cat.get('emoji', '📚'),
                'color': cat.get('color', ''),
                'order': cat.get('order', 0),
            }
        )
    print(f"✅ Migrated {len(categories)} categories")

def migrate_questions(data):
    """Migrate questions"""
    if 'pa_questions' not in data:
        print("❌ No questions found")
        return
    
    questions = data['pa_questions']
    for q in questions:
        category_id = q.get('category', 'umumiy')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            # Create default category if not found
            category = Category.objects.create(
                id=category_id,
                nameUz='Unknown',
                emoji='❓',
                order=99
            )
        
        Question.objects.get_or_create(
            id=q['id'],
            defaults={
                'questionText': q.get('questionText', ''),
                'options': q.get('options', {}),
                'correctAnswer': q.get('correctAnswer', ''),
                'category': category,
            }
        )
    print(f"✅ Migrated {len(questions)} questions")

def migrate_users(data):
    """Migrate users"""
    if 'pa_users' not in data:
        print("❌ No users found")
        return
    
    users = data['pa_users']
    for u in users:
        CustomUser.objects.get_or_create(
            id=u['id'],
            defaults={
                'name': u.get('name', 'Unknown'),
                'fullName': u.get('fullName', ''),
                'phone': u.get('phone', ''),
                'password': u.get('password', ''),
                'role': u.get('role', 'user'),
                'avatar': u.get('avatar', ''),
                'totalPoints': u.get('totalPoints', 0),
            }
        )
    print(f"✅ Migrated {len(users)} users")

def migrate_test_results(data):
    """Migrate test results"""
    if 'pa_results' not in data:
        print("❌ No test results found")
        return
    
    results = data['pa_results']
    for r in results:
        category_id = r.get('category', 'umumiy')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
        
        TestResult.objects.get_or_create(
            id=r['id'],
            defaults={
                'userId': r.get('userId', ''),
                'testDate': r.get('testDate', datetime.now().isoformat()),
                'score': r.get('score', 0),
                'totalQuestions': r.get('totalQuestions', 0),
                'category': category,
                'answers': r.get('answers', {}),
                'duration': r.get('duration'),
            }
        )
    print(f"✅ Migrated {len(results)} test results")

def migrate_chat_messages(data):
    """Migrate chat messages"""
    if 'pa_chat' not in data:
        print("⚠️  No chat messages found")
        return
    
    messages = data['pa_chat']
    for m in messages:
        ChatMessage.objects.get_or_create(
            id=m['id'],
            defaults={
                'senderId': m.get('senderId', ''),
                'conversationId': m.get('conversationId', ''),
                'message': m.get('message', ''),
                'timestamp': m.get('timestamp', datetime.now().isoformat()),
            }
        )
    print(f"✅ Migrated {len(messages)} chat messages")

def migrate_goals(data):
    """Migrate user goals"""
    if 'pa_user_goals' not in data:
        print("⚠️  No goals found")
        return
    
    goals = data['pa_user_goals']
    for g in goals:
        UserGoal.objects.get_or_create(
            id=g.get('id', f"goal_{datetime.now().timestamp()}"),
            defaults={
                'userId': g.get('userId', ''),
                'title': g.get('title', ''),
                'description': g.get('description', ''),
                'completed': g.get('completed', False),
            }
        )
    print(f"✅ Migrated {len(goals)} goals")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate localStorage data to Django')
    parser.add_argument('--file', required=True, help='JSON file with localStorage data')
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"❌ File not found: {args.file}")
        return
    
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Invalid JSON file")
        return
    
    print(f"🚀 Starting migration from {args.file}...\n")
    
    migrate_categories(data)
    migrate_questions(data)
    migrate_users(data)
    migrate_test_results(data)
    migrate_chat_messages(data)
    migrate_goals(data)
    
    print("\n✅ Migration complete!")

if __name__ == '__main__':
    main()
