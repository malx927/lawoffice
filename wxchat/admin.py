from django.contrib import admin, messages
from wxchat.models import MemberRole, WxUserInfo, Menu, WxUnifiedOrderResult, WxPayResult, SwipeImage


admin.site.site_title = "祥子律师后台管理"
admin.site.site_header = "祥子律师事务所"
# admin.site.index_title = "自定义"


@admin.register(MemberRole)
class MemberRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remark']


@admin.register(WxUserInfo)
class WxUserInfoAdmin(admin.ModelAdmin):
    list_display = ['openid', 'nickname', 'sex', 'province', 'city', 'country', 'subscribe', 'subscribe_time']
    search_fields = ['nickname']

    # # 增加自定义按钮
    # actions = ['make_copy', 'custom_button', 'message_test']
    #
    # def custom_button(self, request, queryset):
    #     pass
    #
    # custom_button.short_description = '测试按钮'
    # custom_button.icon = 'fas fa-audio-description'
    # custom_button.type = 'danger'
    # custom_button.style = 'color:black;'
    #
    # def make_copy(self, request, queryset):
    #     pass
    # make_copy.short_description = '复制员工'
    #
    # def message_test(self, request, queryset):
    #     messages.add_message(request, messages.SUCCESS, '操作成功123123123123')
    #
    # # 给按钮增加确认
    # message_test.confirm = '你是否执意要点击这个按钮？'


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(WxUnifiedOrderResult)
class WxUnifiedOrderResultAdmin(admin.ModelAdmin):
    list_display = ('return_code', 'appid', 'mch_id', 'device_info', 'result_code', 'err_code', 'trade_type', 'prepay_id', 'code_url')
    list_per_page = 20


@admin.register(WxPayResult)
class WxPayResultAdmin(admin.ModelAdmin):
    list_display = ('return_code', 'appid', 'mch_id', 'device_info', 'result_code', 'err_code', 'openid',
                    'is_subscribe', 'trade_type', 'total_fee', 'cash_fee', 'transaction_id', 'out_trade_no')


@admin.register(SwipeImage)
class SwipeImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'path', 'sort', 'is_show', 'add_time']
