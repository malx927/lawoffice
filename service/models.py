import datetime

from django.db import models
from django.db.models import Max
from office.models import Office
from wxchat.models import WxUserInfo


class PersonInfo(models.Model):
    """客户信息"""
    openid = models.CharField(verbose_name='微信ID', max_length=120)
    name = models.CharField(verbose_name='姓名', max_length=24)
    telephone = models.CharField(verbose_name='电话', max_length=32)
    id_card = models.CharField(verbose_name='身份证号', max_length=32)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户信息'
        verbose_name_plural = verbose_name


class CompanyInfo(models.Model):
    """公司信息"""
    openid = models.CharField(verbose_name='微信ID', max_length=120)
    name = models.CharField(verbose_name='公司名称', max_length=64)
    credit_code = models.CharField(verbose_name='信用代码', max_length=24)
    address = models.CharField(verbose_name='公司地址', max_length=128)
    legal_person = models.CharField(verbose_name='法人代表', max_length=24)
    telephone = models.CharField(verbose_name='联系方式', max_length=64)
    contact_person = models.CharField(verbose_name='联系人', max_length=32)
    contact_tel = models.CharField(verbose_name='联系方式', max_length=64)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '公司信息'
        verbose_name_plural = verbose_name


class PrivateContract(models.Model):
    """私人律师服务合同"""
    code = models.CharField(verbose_name='合同编号', max_length=16, blank=True, null=True)
    openid = models.CharField(verbose_name='微信ID', max_length=120, blank=True, null=True)
    name = models.CharField(verbose_name='姓名', max_length=24)
    telephone = models.CharField(verbose_name='电话', max_length=32)
    id_card = models.CharField(verbose_name='身份证号', max_length=32)
    office_name = models.CharField(verbose_name='律师名称', max_length=64, blank=True, null=True)
    office_man = models.CharField(verbose_name='联系人', max_length=16, blank=True, null=True)
    office_man_tel = models.CharField(verbose_name='联系电话', max_length=24, blank=True, null=True)
    office_address = models.CharField(verbose_name='地址', max_length=128, blank=True, null=True)
    office_tel = models.CharField(verbose_name='律所电话', max_length=24, blank=True, null=True)
    start_date = models.DateField(verbose_name='开始时间', blank=True, null=True)
    end_date = models.DateField(verbose_name='截止时间', blank=True, null=True)
    is_success = models.BooleanField(verbose_name='生效确认', default=False)
    office_openid = models.CharField(verbose_name='业务人员微信ID', max_length=120, blank=True, null=True)
    # picture = models.ImageField(verbose_name='合同文本', upload_to="contract/", blank=True, null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '私人服务合同'
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]

    @classmethod
    def get_max_code(cls):
        year = datetime.datetime.now().strftime('%Y')
        max_code = cls.objects.filter(code__startswith=year).aggregate(max_code=Max("code"))
        max_value = max_code['max_code']
        if max_value is None:
            num = '0001'
            code = '{0}-{1}'.format(year, num)
            return code
        else:
            num = str(int(max_value[-4:]) + 1).rjust(4, '0')
            code = '{0}-{1}'.format(year, num)
            return code

    def save(self, *args, **kwargs):

        if self.code is None:
            code = PrivateContract.get_max_code()
            self.code = code

        office = Office.objects.first()
        if office:
            self.office_tel = office.telephone

        return super().save(*args, **kwargs)


class CompanyContract(models.Model):
    """公司合同"""
    code = models.CharField(verbose_name='合同编号', max_length=16, blank=True, null=True)
    openid = models.CharField(verbose_name='微信ID', max_length=120, blank=True, null=True)
    name = models.CharField(verbose_name='公司名称', max_length=64)
    credit_code = models.CharField(verbose_name='信用代码', max_length=24)
    address = models.CharField(verbose_name='公司地址', max_length=128)
    legal_person = models.CharField(verbose_name='法人代表', max_length=24)
    telephone = models.CharField(verbose_name='联系电话', max_length=64)
    contact_person = models.CharField(verbose_name='联系人', max_length=32)
    contact_tel = models.CharField(verbose_name='联系电话', max_length=64)
    office_name = models.CharField(verbose_name='律师名称', max_length=64, blank=True, null=True)
    office_code = models.CharField(verbose_name='信用代码', max_length=24, blank=True, null=True)
    office_man = models.CharField(verbose_name='联系人', max_length=16, blank=True, null=True)
    office_man_tel = models.CharField(verbose_name='联系电话', max_length=24, blank=True, null=True)
    office_address = models.CharField(verbose_name='地址', max_length=128, blank=True, null=True)
    office_tel = models.CharField(verbose_name='律所电话', max_length=24, blank=True, null=True)
    start_date = models.DateField(verbose_name='开始时间', blank=True, null=True)
    end_date = models.DateField(verbose_name='截止时间', blank=True, null=True)
    is_success = models.BooleanField(verbose_name='生效确认', default=False)
    office_openid = models.CharField(verbose_name='业务人员微信ID', max_length=120, blank=True, null=True)
    money = models.IntegerField(verbose_name='合同金额', default=0)
    # picture = models.ImageField(verbose_name='合同文本', upload_to="contract/", blank=True, null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '法律顾问合同'
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]

    @classmethod
    def get_max_code(cls):
        year = datetime.datetime.now().strftime('%Y')
        max_code = cls.objects.filter(code__startswith=year).aggregate(max_code=Max("code"))
        max_value = max_code['max_code']
        if max_value is None:
            num = '0001'
            code = '{0}-{1}'.format(year, num)
            return code
        else:
            num = str(int(max_value[-4:]) + 1).rjust(4, '0')
            code = '{0}-{1}'.format(year, num)
            return code

    def save(self, *args, **kwargs):
        if self.code is None:
            code = CompanyContract.get_max_code()
            self.code = code

        office = Office.objects.first()
        if office:
            if self.office_name is None:
                self.office_name = office.name
                self.office_code = office.credit_code
                self.office_address = office.address
                self.office_tel = office.telephone

        # if self.office_openid:
        #     office_user = WxUserInfo.objects.filter(openid=self.office_openid).first()
        #     if office_user:
        #         self.office_man = office_user.name
        #         self.office_man_tel = office_user.telephone

        return super().save(*args, **kwargs)


class ContractAmount(models.Model):
    """合同金额列表"""
    money = models.IntegerField(verbose_name='金额', default=0)
    desc = models.CharField(verbose_name='说明', max_length=256, blank=True, null=True)
    sort = models.IntegerField(verbose_name='排序', default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    def __str__(self):
        return str(self.money)

    class Meta:
        verbose_name = '合同金额列表'
        verbose_name_plural = verbose_name
        ordering = ['sort']



