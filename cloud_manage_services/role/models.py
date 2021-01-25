from django.db import models


class Role(models.Model):
    """
    角色
    """

    class Meta:
        db_table = 'role'

    name = models.CharField('名称', max_length=64)
