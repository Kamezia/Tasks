from .views import TaskViewSet, UserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]