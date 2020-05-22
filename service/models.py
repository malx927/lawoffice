from django.db import models


class PersonInfo(models.Model):
    """客户信息"""
    openid = models.CharField(verbose_name='微信ID', max_length=120)
    name = models.CharField(verbose_name='姓名', max_length=24)
    telephone = models.CharField(verbose_name='电话', max_length=32)
    id_card = models.CharField(verbose_name='身份证号', max_length=32)
    client = models.CharField(verbose_name='委托人', max_length=24)
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
    code = models.CharField(verbose_name='合同编号', max_length=16)
    openid = models.CharField(verbose_name='微信ID', max_length=120, blank=True, null=True)
    name = models.CharField(verbose_name='姓名', max_length=24)
    telephone = models.CharField(verbose_name='电话', max_length=32)
    id_card = models.CharField(verbose_name='身份证号', max_length=32)
    client = models.CharField(verbose_name='委托人', max_length=24)
    office_name = models.CharField(verbose_name='律师名称', max_length=64)
    office_man = models.CharField(verbose_name='联系人', max_length=16)
    office_man_tel = models.CharField(verbose_name='联系电话', max_length=24)
    office_address = models.CharField(verbose_name='地址', max_length=128)
    start_date = models.DateField(verbose_name='开始时间')
    end_date = models.DateField(verbose_name='截止时间')
    sign_date = models.DateTimeField(verbose_name='签订时间')
    is_success = models.BooleanField(verbose_name='生效确认', default=False)
    success_date = models.DateTimeField(verbose_name='生效时间', blank=True, null=True)
    picture = models.ImageField(verbose_name='合同文本', upload_to="contract/", blank=True, null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '私人服务合同'
        verbose_name_plural = verbose_name


class CompanyContract(models.Model):
    """公司合同"""
    code = models.CharField(verbose_name='合同编号', max_length=16)
    openid = models.CharField(verbose_name='微信ID', max_length=120, blank=True, null=True)
    company = models.ForeignKey(CompanyInfo, verbose_name='公司ID', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(verbose_name='公司名称', max_length=64)
    credit_code = models.CharField(verbose_name='信用代码', max_length=24)
    address = models.CharField(verbose_name='公司地址', max_length=128)
    legal_person = models.CharField(verbose_name='法人代表', max_length=24)
    telephone = models.CharField(verbose_name='联系方式', max_length=64)
    contact_person = models.CharField(verbose_name='联系人', max_length=32)
    contact_tel = models.CharField(verbose_name='联系方式', max_length=64)
    office_name = models.CharField(verbose_name='律师名称', max_length=64)
    office_code = models.CharField(verbose_name='信用代码', max_length=24)
    office_man = models.CharField(verbose_name='联系人', max_length=16)
    office_man_tel = models.CharField(verbose_name='联系电话', max_length=24)
    office_address = models.CharField(verbose_name='地址', max_length=128)
    start_date = models.DateField(verbose_name='开始时间')
    end_date = models.DateField(verbose_name='截止时间')
    sign_date = models.DateTimeField(verbose_name='签订时间')
    is_confirm = models.BooleanField(verbose_name='收费确认', default=False)
    confirm_date = models.DateTimeField(verbose_name='确认时间', blank=True, null=True)
    is_success = models.BooleanField(verbose_name='生效确认', default=False)
    success_date = models.DateTimeField(verbose_name='生效时间', blank=True, null=True)
    picture = models.ImageField(verbose_name='合同文本', upload_to="contract/", blank=True, null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '法律顾问合同'
        verbose_name_plural = verbose_name
