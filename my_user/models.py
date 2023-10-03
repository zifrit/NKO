from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    middle_name = models.CharField(max_length=255, verbose_name='фамилия')
    JOBS = (
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
    )
    job = models.CharField(max_length=20, choices=JOBS, verbose_name='Должность', default='Frontend')
    description = models.TextField(blank=True, verbose_name='Доп.Инфо')

    class Meta:
        db_table = 'UserProfile'
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def get_full_name(self):
        full_name = f'{self.user.get_full_name()} {self.middle_name}'
        return full_name
