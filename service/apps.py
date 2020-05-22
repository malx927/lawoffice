from django.apps import AppConfig


class ServiceConfig(AppConfig):
    name = 'service'
    verbose_name = '律师服务'

    def ready(self):
        from .signals import update_persion_info


