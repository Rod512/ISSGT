from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Unread tracking

    def __str__(self):
        return self.name

    @staticmethod
    def delete_old_messages():
        threshold_date = now() - timedelta(days=30)
        Contact.objects.filter(created_at__lt=threshold_date).delete()
