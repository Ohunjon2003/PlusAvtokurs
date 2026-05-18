from django.contrib import admin
from .models import (
    Category, Question, TestResult, CustomUser, ActivityLog,
    ChatMessage, UserGoal, Bookmark, StudyMaterial, Notification
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'nameUz', 'emoji', 'order')
    ordering = ['order']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'questionText', 'category', 'createdAt')
    search_fields = ('questionText',)
    list_filter = ('category', 'createdAt')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'userId', 'category', 'score', 'totalQuestions', 'testDate')
    search_fields = ('userId',)
    list_filter = ('category', 'testDate')
    readonly_fields = ('createdAt',)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fullName', 'phone', 'role', 'totalPoints', 'createdAt')
    search_fields = ('name', 'phone', 'fullName')
    list_filter = ('role', 'createdAt')
    readonly_fields = ('id', 'createdAt')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('userId', 'action', 'timestamp')
    search_fields = ('userId', 'action')
    list_filter = ('timestamp',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'senderId', 'conversationId', 'timestamp')
    search_fields = ('senderId', 'conversationId')
    list_filter = ('timestamp',)

@admin.register(UserGoal)
class UserGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'userId', 'completed', 'createdAt')
    search_fields = ('userId', 'title')
    list_filter = ('completed', 'createdAt')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('userId', 'questionId', 'createdAt')
    search_fields = ('userId',)

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'createdAt')
    search_fields = ('title',)
    list_filter = ('category', 'createdAt')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('userId', 'title', 'read', 'createdAt')
    search_fields = ('userId', 'title')
    list_filter = ('read', 'createdAt')
