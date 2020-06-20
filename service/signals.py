
# 私人律师
from django.db.models.signals import post_save
from django.dispatch import receiver
from service.models import PrivateContract, PersonInfo, CompanyContract, CompanyInfo


@receiver(post_save, sender=PrivateContract)
def update_persion_info(sender, instance, created, **kwargs):

    if instance.openid:
        user_info = {
            'name': instance.name,
            'telephone': instance.telephone,
            'id_card': instance.id_card,
        }
        obj, created = PersonInfo.objects.update_or_create(defaults=user_info, openid=instance.openid)
        print(obj, created)


@receiver(post_save, sender=CompanyContract)
def update_company_info(sender, instance, created, **kwargs):
    if instance.openid:
        company_info = {
            'name': instance.name,
            # 'telephone': instance.telephone,
            # 'credit_code': instance.credit_code,
            # 'address': instance.address,
            # 'legal_person': instance.legal_person,
            'contact_person': instance.contact_person,
            'contact_tel': instance.contact_tel,
        }
        obj, created = CompanyInfo.objects.update_or_create(defaults=company_info, openid=instance.openid)
        print(obj, created)
