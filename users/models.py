from distutils.command.upload import upload
from operator import mod
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Класс пользователя sreda.media'''
    tg_username = models.TextField(
        verbose_name='Username пользователя в telegram',
        null=False,
        unique=True) 
    tg_id = models.PositiveIntegerField(
        verbose_name='Id пользователя в telegram',
        null=False,
        unique=True)
    # tg_pic = models.ImageField(max_lenght=300, upload_to='images/user_pic')


