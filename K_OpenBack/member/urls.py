# -*- coding: utf-8 -*-

from django.urls import path
from . import views
# http://127.0.0.1:8000/member/
urlpatterns=[
    #http://127.0.0.1:8000/member/s3Upload/ 요청시 view.py
    #  의 s3Upload 함수 실행
    path("s3Upload/", views.s3Upload, name="s3Upload"),
    path("s3Download/", views.s3Upload, name="s3Download"),
    path("join/", views.join, name="join"),
    path("login/", views.login, name="login"),
]