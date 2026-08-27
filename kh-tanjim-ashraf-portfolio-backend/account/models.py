from django.db import models
from django.contrib.auth.models import User
from shared.models import TimestampMixins
from django.core.validators import MaxValueValidator, URLValidator



class Profile(TimestampMixins):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150)
    headline = models.CharField(max_length=100)
    bio = models.TextField()
    phone = models.CharField(max_length=17)
    location = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='account/avatar/', blank=True, null=True)
    resume = models.FileField(upload_to='account/document/')
    github_url = models.URLField(max_length=255, blank=True, null=True, validators=[URLValidator(schemes=['https'])])
    linkedin_url = models.URLField(max_length=255, blank=True, null=True, validators=[URLValidator(schemes=['https'])])
    x_url = models.URLField(max_length=255, blank=True, null=True, validators=[URLValidator(schemes=['https'])])
    website_url = models.URLField(max_length=255, blank=True, null=True, validators=[URLValidator(schemes=['https'])])
    years_of_experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(30)])
    is_available_for_hire = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name