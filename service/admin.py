from django.contrib import admin
from service.models import PersonInfo, CompanyInfo, PrivateContract, CompanyContract, ContractAmount, \
    PrivateContractAmount


@admin.register(PersonInfo)
class PersonInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'telephone', 'id_card', 'add_time']
    search_fields = ['name', 'telephone', 'id_card']
    list_filter = ['add_time']


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'contact_tel', 'add_time']
    search_fields = ['name', 'contact_tel', 'contact_person']
    list_filter = ['add_time']


@admin.register(PrivateContract)
class PrivateContractAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'telephone', 'start_date', 'end_date', 'money', 'is_success']
    search_fields = ['code', 'name', 'telephone', 'id_card']
    list_filter = ['start_date', 'is_success']
    # readonly_fields = ['code']

    fieldsets = (
        (None, {
            'fields': ('code', ('start_date', 'end_date'))
        }),
        ('客户信息', {
            'fields': (('name', 'id_card'), 'telephone')
        }),
        ('律所信息', {
            'fields': (('office_name', 'office_man'), ('office_address', 'office_man_tel'))
        }),
        ('其他信息', {
            'fields': ('is_success', 'openid', 'office_openid')
        })

    )


@admin.register(CompanyContract)
class CompanyContractAdmin(admin.ModelAdmin):

    list_display = ['code', 'name', 'contact_person', 'contact_tel', 'start_date', 'end_date', 'is_success']
    search_fields = ['code', 'name', 'contact_person', 'contact_tel']
    list_filter = ['is_success']
    # readonly_fields = ['code']

    fieldsets = (
        (None, {
            'fields': ('code', ('start_date', 'end_date'))
        }),
        ('公司信息', {
            'fields': ('name', 'contact_person', 'contact_tel')
        }),
        ('律所信息', {
            'classes': ('collapse',),
            'fields': ('office_name', 'office_man', 'office_man_tel', 'office_address')
        }),
        ('其他信息', {
            'classes': ('collapse',),
            'fields': ('is_success', 'openid', 'office_openid')
        })

    )

    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
            'all': ('css/admin/service.css',)
        }


@admin.register(ContractAmount)
class ContractAmountAdmin(admin.ModelAdmin):

    list_display = ['money', 'desc', 'sort', 'add_time']
    search_fields = ['money', 'desc']


@admin.register(PrivateContractAmount)
class PrivateContractAmountAdmin(admin.ModelAdmin):

    list_display = ['money', 'desc', 'add_time']
    search_fields = ['money', 'desc']
