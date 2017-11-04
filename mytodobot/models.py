import uuid

from django.db import models


class Task(models.Model):
    userid = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return str(self.createdAt)
