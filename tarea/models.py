from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    task_type  = models.CharField(max_length=255, null=False, blank=False)
    task_highlites = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name