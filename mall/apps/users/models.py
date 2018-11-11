from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    """
    User Model
    """
    mobile = models.CharField(max_length=11, unique=True)
    email_active = models.BooleanField(default=False, verbose_name='邮箱是否验证')

    class Meta:
        db_table = 'tb_user'
        verbose_name = 'user'
