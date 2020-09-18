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
    path('testlist/', views.testlist, name='testlist'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('checkuser/', views.checkuser, name='checkuser'),
    path('checkemail/', views.checkemail, name='checkemail'),
    path('logout/', views.logout, name='logout'),
    path('activate/', views.activate, name='activate'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/', views.delete_from_cart, name='delete_from_cart'),
    path('change_select_state/', views.change_select_state, name='change_select_state'),
    path('delete_in_cart/', views.delete_in_cart, name='delete_in_cart'),
    path('add_in_cart/', views.add_in_cart, name='add_in_cart'),
    path('cart_all_unselect/', views.cart_all_unselect, name='cart_all_unselect'),
    path('cart_all_select/', views.cart_all_select, name='cart_all_select'),
    path('make_order/', views.make_order, name='make_order'),
    path('orderdetails/', views.orderdetails, name='orderdetails'),
]
