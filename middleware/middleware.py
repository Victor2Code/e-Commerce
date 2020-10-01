#! /usr/bin/env python
# -*- coding: utf-8 -*- 
# @author: xiaofu
# @date: 2020-Sep-15
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import User


class loginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        paths_for_json = [
            '/shop/add_to_cart/',
            '/shop/delete_from_cart/',
            '/shop/change_select_state/',
            '/shop/cart_all_unselect/',
            '/shop/cart_all_select/',
            '/shop/delete_in_cart/',
            '/shop/add_in_cart/',
            '/shop/make_order/',
        ]
        paths_for_html = [
            '/shop/market/',
            '/shop/cart/',
            '/shop/orderdetails/',
            '/shop/mine/',
            '/shop/orderlist_not_pay/',
        ]
        if request.path in paths_for_json:
            username = request.session.get('username')
            if username:
                user = User.objects.filter(username=username)
                if user.exists():
                    request.user = user.first()
            else:
                data={
                    'status': 701,
                    'message': 'User Not Found',
                }
                return JsonResponse(data)
        if request.path in paths_for_html:
            username = request.session.get('username')
            if username:
                user = User.objects.filter(username=username)
                if user.exists():
                    request.user = user.first()
            else:
                return HttpResponseRedirect(reverse('shop:login'))
