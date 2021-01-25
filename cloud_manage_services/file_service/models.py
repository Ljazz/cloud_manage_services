from django.db import models


class FileService(models.Model):
    """
    文件服务
    """

    class Meta:
        db_table = 'file_server'

    name = models.CharField('文件名称', max_length=64, null=True)
    path = models.CharField('文件链接', max_length=128)
    type = models.CharField('文件类型', max_length=8, null=True)
    size = models.CharField('文件大小', max_length=8, null=True)
    note = models.TextField('备注', default='')
    is_active = models.BooleanField('状态', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)
