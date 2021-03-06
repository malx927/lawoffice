"""lawoffice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from wxchat.views import wechat, createMenu, getMenu, deleteMenu, getWechatAuth, getWechatAuthCode, get_user_info

urlpatterns = [
    path('', wechat),  # 微信入口
    path('createmenu/', createMenu, name='wxchat-create-menu'),
    path('getmenu/', getMenu, name='wxchat-get-menu'),
    path('delmenu/', deleteMenu, name='wxchat-delete-menu'),
    path('auth_code/', getWechatAuthCode, name='wxchat-auth-code'),
    path('auth_openid/', getWechatAuth, name='wxchat-auth-openid'),
    path('userinfo/', get_user_info, name='wxchat-user-info'),
]
