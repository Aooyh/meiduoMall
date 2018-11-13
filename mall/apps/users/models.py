from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.


class User(AbstractUser):

    """
    User Model
    """
    mobile = models.CharField(max_length=11, unique=True)
    email_active = models.BooleanField(default=False, verbose_name='邮箱是否验证')
    default_add = models.ForeignKey('users.Address', on_delete=models.CASCADE, verbose_name='默认地址',
                                    null=True, blank=True)

    class Meta:
        db_table = 'tb_user'
        verbose_name = 'user'


class Address(models.Model):
    user_id = models.ForeignKey(User, verbose_name='用户', on_delete=models.SET_NULL, null=True)
    receiver = models.CharField(max_length=10, verbose_name='收货人')
    mobile = models.CharField(max_length=11, verbose_name='联系手机', null=True)
    email = models.EmailField(verbose_name='联系邮箱', null=True)
    tel = models.CharField(max_length=10, null=True, verbose_name='固定电话')
    province = models.ForeignKey('areas.Area', verbose_name='省', related_name='province')
    city = models.ForeignKey('areas.Area', verbose_name='市', related_name='city')
    district = models.ForeignKey('areas.Area', verbose_name='县/区', related_name='district')
    place = models.CharField(max_length=50, verbose_name='详细地址')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    update_time = models.DateField(auto_now=True, verbose_name='更新时间')
    create_time = models.DateField(verbose_name='创建时间', default=datetime.now())

    class Meta:
        db_table = 'tb_user_add'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
