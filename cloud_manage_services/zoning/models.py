from django.db import models


class Zoning(models.Model):
    """
    行政区划
    """
    class Meta:
        db_table = 'zoning'

    name = models.CharField('名称', max_length=32)
    code = models.CharField('编码', max_length=32)
    level = models.PositiveIntegerField('行政级别', default=0)
    prefix = models.CharField('区号', max_length=8, null=True)
    post_code = models.CharField('邮政编号', max_length=8, null=True)
    abbreviation = models.CharField('简称', max_length=8, null=True)
    administrative_center = models.CharField('行政中心', max_length=32, null=True)
    is_active = models.BooleanField('状态', default=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    update_date = models.DateTimeField('更新时间', auto_now=True)
    parent = models.ForeignKey('zoning.Zoning',
                               on_delete=models.SET_NULL,
                               null=True)
