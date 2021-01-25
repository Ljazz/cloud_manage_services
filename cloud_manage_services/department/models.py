from django.db import models


class Department(models.Model):
    """
    部门
    """
    class Meta:
        db_table = 'department'

    code = models.CharField('编码', max_length=32)
    name = models.CharField('名称', max_length=32)
    abbreviation = models.CharField('简称', max_length=32, null=True)
    fax = models.CharField('传真', max_length=32, null=True)
    website = models.CharField('网址', max_length=32, null=True)
    is_active = models.NullBooleanField('状态', max_length=1, default=1)  # 1 有效， 0 无效
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    update_date = models.DateTimeField('更新时间', auto_now=True)
    parent = models.ForeignKey('department.Department',
                               verbose_name='父级机构',
                               on_delete=models.SET_NULL,
                               null=True)