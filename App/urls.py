#! /usr/bin/env python
# -*- coding: utf-8 -*- 
# @author: xiaofu
# @date: 2020-Aug-16
from django.urls import path, include

from App import views
from Shop import settings

urlpatterns = [
    path('home/', views.home, name='home'),
    path('market/', views.market, name='market'),
    path('cart/', views.cart, name='cart'),
    path('mine/', views.mine, name='mine'),
    path('test/', views.test, name='test'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('checkuser/', views.checkuser, name='checkuser'),
    path('checkemail/', views.checkemail, name='checkemail'),
    path('logout/', views.logout, name='logout'),
]
