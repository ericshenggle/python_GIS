"""GIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import re_path

from . import views

urlpatterns = [
    re_path("admin", admin.site.urls),                  # Django用户管理界面
    re_path("date", views.date),                        # 获取查询特定日期的POST请求
    re_path("show_map", views.show_map),                # 重定向至特定日期的分布图
    re_path("hello", views.airQualityInfoToday),        # 获取页面初始化的GET请求
    re_path("detail", views.airQualityInfoDetail)       # 获取特定城市过去五日数据的POST请求
]
