from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from course.views import (register, CourseViewSet, UserViewSet, PostViewSet, ReplyViewSet, ChatView, DashBoardView,
                          StudyPlanView, QuizViewSet)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'replies', ReplyViewSet, basename='reply')
router.register(r'quizzes', QuizViewSet, basename='quiz')
urlpatterns = [
    path('api/auth/register', register),
    path('api/auth/login', TokenObtainPairView.as_view()),
    path('admin', admin.site.urls),
    path("api/", include(router.urls), name="api"),
    path("api/chat", ChatView.as_view(), name="chat"),
    path("api/dashboard", DashBoardView.as_view(), name="dashboard"),
    path("api/studyplan", StudyPlanView.as_view(), name="studyplan"),
]
