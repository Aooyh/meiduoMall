from django.db import models

# Create your models here.


class Area(models.Model):
    """
    行政区划
    """
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs',
                               verbose_name='上级行政区划', blank=True, null=True)

    class Meta:
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'
        db_table = 'tb_areas'

    def __str__(self):
        return self.name
