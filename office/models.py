from django.db import models


class Office(models.Model):
    """律师事务所"""
    name = models.CharField(verbose_name='名称', max_length=120)
    credit_code = models.CharField(verbose_name='信用代码', max_length=20, blank=True, null=True)
    address = models.CharField(verbose_name='律所所在市', max_length=150, blank=True)
    legal_person = models.CharField(verbose_name='法定代表人', max_length=20, blank=True, null=True)
    telephone = models.CharField(verbose_name='联系电话', max_length=30, blank=True, null=True)
    position = models.CharField(verbose_name='所在地', max_length=150, blank=True)
    bank = models.CharField(verbose_name='开户行', max_length=60, blank=True, null=True)
    account = models.CharField(verbose_name='银行账号', max_length=20, blank=True, null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    add_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '律师事务所'
        verbose_name_plural = '律师事务所'

    def __str__(self):
        return self.name
