from rest_framework import viewsets
from .serializers import  UserSerializer, TaskWriteOnlySerializer, TaskReadOnlySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Task
from django.contrib.auth.models import  User



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskWriteOnlySerializer
        return TaskReadOnlySerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            return Task.objects.filter(user_id=user_id)
        return Task.objects.all()

    
    def update(self, request, *args, **kwargs):
        task = self.get_object() # This an instance from Task table.
        if task.user != request.user:
            raise PermissionDenied("You do not have permission to edit this task.")
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != request.user:
            raise PermissionDenied("You do not have permission to delete this task.")
        return super().destroy(request, *args, **kwargs)