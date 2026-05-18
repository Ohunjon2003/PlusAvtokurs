from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import json

class Category(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nameUz = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'categories'
        ordering = ['order']
    
    def __str__(self):
        return self.nameUz

class Question(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    questionText = models.TextField()
    options = models.JSONField()
    correctAnswer = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='questions')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
    
    def __str__(self):
        return self.questionText[:50]

class TestResult(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    userId = models.CharField(max_length=100)
    testDate = models.DateTimeField()
    score = models.IntegerField()
    totalQuestions = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    answers = models.JSONField(default=dict)
    duration = models.IntegerField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'test_results'
        indexes = [
            models.Index(fields=['userId', '-testDate']),
        ]
    
    def __str__(self):
        return f"{self.userId} - {self.category} ({self.score}/{self.totalQuestions})"

class CustomUser(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    fullName = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    avatar = models.URLField(blank=True, null=True)
    totalPoints = models.IntegerField(default=0)
    lastActive = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'custom_users'
    
    def __str__(self):
        return f"{self.name} ({self.role})"

class ActivityLog(models.Model):
    userId = models.CharField(max_length=100)
    action = models.CharField(max_length=200)
    details = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activity_logs'
    
    def __str__(self):
        return f"{self.userId}: {self.action}"

class ChatMessage(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    senderId = models.CharField(max_length=100)
    conversationId = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField()
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.senderId}: {self.message[:50]}"

class UserGoal(models.Model):
    userId = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    completedDate = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_goals'
    
    def __str__(self):
        return self.title

class Bookmark(models.Model):
    userId = models.CharField(max_length=100)
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bookmarks'
        unique_together = ('userId', 'questionId')
    
    def __str__(self):
        return f"{self.userId} - {self.questionId}"

class StudyMaterial(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    imageUrl = models.URLField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'study_materials'
    
    def __str__(self):
        return self.title

class Notification(models.Model):
    userId = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    message = models.TextField()
    read = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
    
    def __str__(self):
        return f"{self.userId}: {self.title}"
