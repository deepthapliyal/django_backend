# notes/models.py
from django.db import models
from users.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Change '1' to the appropriate user ID as your default value
    title = models.CharField(max_length=255)
    content = models.TextField()
    color = models.CharField(max_length=10, default="white")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
