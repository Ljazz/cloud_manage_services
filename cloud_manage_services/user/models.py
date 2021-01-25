from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    用户
    """

    class Meta:
        db_table = 'user'

    nickname = models.CharField('昵称', max_length=32, null=True)
    name = models.CharField('姓名', max_length=64, null=True)
    gender = models.CharField('性别', max_length=8, null=True)
    nation = models.CharField('民族', max_length=16, null=True)
    birthday = models.CharField('生日', max_length=32, null=True)
    job_title = models.CharField('职称', max_length=16, null=True)
    mobile = models.CharField('手机号码', max_length=16, null=True)
    marital_status = models.CharField('婚姻状况', max_length=8, null=True)
    address = models.CharField('通讯地址', max_length=128, null=True)
    postcode = models.CharField('邮编', max_length=16, null=True)
    degree = models.CharField('学位', max_length=16, null=True)
    graduation_school = models.CharField('毕业院校', max_length=32, null=True)
    graduation_time = models.CharField('毕业时间', max_length=32, null=True)
    hobby = models.TextField('爱好', default='')
    note = models.TextField('备注', default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    avatar = models.OneToOneField('file_service.FileService',
                                  on_delete=models.SET_NULL,
                                  verbose_name='头像',
                                  null=True)
    location = models.ForeignKey('zoning.Zoning',
                                 on_delete=models.SET_NULL,
                                 verbose_name='所在地',
                                 null=True)
    department = models.ForeignKey('department.Department',
                                   on_delete=models.SET_NULL,
                                   verbose_name='部门',
                                   null=True)
    role = models.ManyToManyField('role.Role',
                                  verbose_name='角色')
