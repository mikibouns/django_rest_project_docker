from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    '''Пользователи'''
    fio = models.CharField(max_length=256, blank=True, null=True)
    address = models.EmailField()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username