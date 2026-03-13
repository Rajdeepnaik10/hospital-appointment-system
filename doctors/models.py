from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username