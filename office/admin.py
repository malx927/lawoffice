from django.contrib import admin
from office.models import Office


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ['name', 'telephone', 'credit_code', 'address', 'legal_person', 'position', 'bank', 'account', 'add_time']
    search_fields = ['name', 'telephone', 'credit_code', 'legal_person']
