from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from datetime import datetime
import hashlib
from .models import (
    Category, Question, TestResult, CustomUser, ActivityLog,
    ChatMessage, UserGoal, Bookmark, StudyMaterial, Notification
)
from .serializers import (
    CategorySerializer, QuestionSerializer, TestResultSerializer,
    CustomUserSerializer, CustomUserDetailSerializer, ActivityLogSerializer,
    ChatMessageSerializer, UserGoalSerializer, BookmarkSerializer,
    StudyMaterialSerializer, NotificationSerializer
)

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category')
        if category_id:
            questions = Question.objects.filter(category_id=category_id)
            serializer = self.get_serializer(questions, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user_id = request.query_params.get('userId')
        if user_id:
            results = TestResult.objects.filter(userId=user_id).order_by('-testDate')
            serializer = self.get_serializer(results, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        user_id = request.query_params.get('userId')
        category_id = request.query_params.get('category')
        if user_id and category_id:
            results = TestResult.objects.filter(
                userId=user_id, category_id=category_id
            ).order_by('-testDate')
            serializer = self.get_serializer(results, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        
        if not name or not password:
            return Response(
                {'error': 'Username and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        hashed = hash_password(password)
        user = CustomUser.objects.filter(name=name, password=hashed).first()
        
        if user:
            serializer = CustomUserDetailSerializer(user)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        fullName = request.data.get('fullName', '')
        phone = request.data.get('phone', '')
        
        if CustomUser.objects.filter(name=name).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if CustomUser.objects.filter(phone=phone).exists():
            return Response(
                {'error': 'Phone already registered'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = CustomUser.objects.create(
            id=f'user_{datetime.now().timestamp()}',
            name=name,
            fullName=fullName,
            phone=phone,
            password=hash_password(password),
            role='user'
        )
        
        serializer = CustomUserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        phone = request.data.get('phone')
        new_password = request.data.get('newPassword')
        
        user = CustomUser.objects.filter(phone=phone).first()
        if not user:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user.password = hash_password(new_password)
        user.save()
        
        return Response({'message': 'Password reset successfully'})

class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def log_activity(self, request):
        user_id = request.data.get('userId')
        action = request.data.get('action')
        details = request.data.get('details', {})
        
        log = ActivityLog.objects.create(
            userId=user_id,
            action=action,
            details=details
        )
        
        serializer = self.get_serializer(log)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def by_conversation(self, request):
        conversation_id = request.query_params.get('conversationId')
        if conversation_id:
            messages = ChatMessage.objects.filter(
                conversationId=conversation_id
            ).order_by('timestamp')
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)

class UserGoalViewSet(viewsets.ModelViewSet):
    queryset = UserGoal.objects.all()
    serializer_class = UserGoalSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user_id = request.query_params.get('userId')
        if user_id:
            goals = UserGoal.objects.filter(userId=user_id)
            serializer = self.get_serializer(goals, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user_id = request.query_params.get('userId')
        if user_id:
            bookmarks = Bookmark.objects.filter(userId=user_id)
            serializer = self.get_serializer(bookmarks, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)

class StudyMaterialViewSet(viewsets.ModelViewSet):
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category')
        if category_id:
            materials = StudyMaterial.objects.filter(category_id=category_id)
            serializer = self.get_serializer(materials, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user_id = request.query_params.get('userId')
        if user_id:
            notifications = Notification.objects.filter(userId=user_id).order_by('-createdAt')
            serializer = self.get_serializer(notifications, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)
