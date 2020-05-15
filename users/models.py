from django.db import models
import datetime
from django.contrib.auth.hashers import make_password, check_password

class Post(models.Model):
    """用户类型"""
    id = models.IntegerField(verbose_name='编号', primary_key=True)
    name = models.CharField(verbose_name='类型名称', max_length=50)

    class Meta:
        verbose_name = '用户类型'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    权限表
    """
    LEVEL = (
        (0, '一级'),
        (1, '二级'),
        (2, '三级'),
    )
    name = models.CharField(verbose_name='名称', max_length=64)
    path = models.CharField(verbose_name='链接地址', max_length=256, blank=True, null=True)
    level = models.IntegerField(verbose_name='层级', default=0, choices=LEVEL)
    parent = models.ForeignKey(verbose_name='父级', to='self', related_name='perms', null=True, blank=True, on_delete=models.SET_NULL)
    sort = models.IntegerField(verbose_name='排序', default=0)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限信息'
        verbose_name_plural = verbose_name
        ordering = ['-create_at']


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(verbose_name='角色名称', max_length=32)
    comment = models.CharField(verbose_name='角色说明', max_length=128, blank=True, null=True)
    permissions = models.ManyToManyField(verbose_name='权限', to='Permission', blank=True)
    only_own = models.BooleanField(verbose_name='只看自己内容', default=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural = verbose_name
        ordering = ['-create_at']


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='登录名', max_length=32, unique=True)
    real_name = models.CharField(verbose_name='姓名', max_length=32)
    gender = models.IntegerField(verbose_name="性别", choices=((1, "男"), (2, "女")), blank=True, null=True)
    password = models.CharField(verbose_name='密码', max_length=128)
    telephone = models.CharField(verbose_name='手机', max_length=16)
    post = models.ForeignKey(Post, verbose_name="用户类型", on_delete=models.SET_NULL, null=True, blank=True)
    job = models.CharField(verbose_name="职务", max_length=64, blank=True, null=True)
    job_time = models.DateField(verbose_name="执业时间", blank=True, null=True)
    license_num = models.CharField(verbose_name="律师证号", max_length=32, blank=True, null=True)
    prof_title = models.CharField(verbose_name="律师职称", max_length=64, blank=True, null=True)
    is_superuser = models.BooleanField(verbose_name='超级管理员', default=False)
    is_active = models.BooleanField(verbose_name='是否有效', default=True)
    date_joined = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='最近登录时间', blank=True, null=True)
    is_update = models.BooleanField(verbose_name="是否完善", default=False)
    roles = models.ManyToManyField(verbose_name='所属角色', to='Role', blank=True)

    def __str__(self):
        return self.real_name if self.real_name else self.name

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def practice_years(self):
        if self.job_time:
            return datetime.datetime.now().year - self.job_time.year
        else:
            return 0

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
