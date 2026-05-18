from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, QuestionViewSet, TestResultViewSet,
    CustomUserViewSet, ActivityLogViewSet, ChatMessageViewSet,
    UserGoalViewSet, BookmarkViewSet, StudyMaterialViewSet,
    NotificationViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'test-results', TestResultViewSet)
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'activity-logs', ActivityLogViewSet)
router.register(r'chat-messages', ChatMessageViewSet)
router.register(r'goals', UserGoalViewSet)
router.register(r'bookmarks', BookmarkViewSet)
router.register(r'study-materials', StudyMaterialViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
