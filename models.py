from django.db import models
from django.contrib.auth.models import User

class MessageLog(models.Model):

    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    branch = models.CharField(max_length=100)
    document = models.CharField(max_length=100)

    loan = models.IntegerField(null=True, blank=True)
    fees = models.IntegerField(null=True, blank=True)
    credit = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} - {self.mobile}"