from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    middle_name = models.CharField(max_length=255, verbose_name='фамилия')

    class Meta:
        db_table = 'UserProfile'
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def get_full_name(self):
        full_name = f'{self.user.get_full_name()} {self.middle_name}'
        return full_name
