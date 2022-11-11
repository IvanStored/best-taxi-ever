from django.conf import settings
from django.db import models


class ThreadModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    has_unread = models.BooleanField(default=False)


class MessageModel(models.Model):
    thread = models.ForeignKey(
        "ThreadModel",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    sender_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    receiver_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    body = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
