from django.db import models
from shared.models import TimestampMixins



class ContactMessage(TimestampMixins):
    name = models.CharField(max_length=150)
    email = models.EmailField() # Default max_length=254
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}---{self.email}---{self.subject}'