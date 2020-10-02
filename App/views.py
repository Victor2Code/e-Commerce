import os
import random
import traceback
import uuid

from alipay import AliPayConfig, AliPay
from django.core.cache import cache, caches
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from multiprocessing import Process

# Create your views here.
# from App.models import Test


# def test(request):
#     img = Test.objects.filter(name='test1')
#     context = {
#         'img': img
#     }
#     return render(request, 'test.html', context=context)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from App.models import MainSwiper, MainNav, MainMustBuy, GoodType, Goods, User, Cart, Order, OrderGoods
from App.tools import my_password_generator, my_password_checker, send_verification_email, total_price
from Shop.settings import MEDIA_ROOT_PREFIX, BASE_DIR


def home(request):
    swiper_imgs = MainSwiper.objects.all()
    nav_imgs = MainNav.objects.all()
    mustbuy_imgs = MainMustBuy.objects.all()
    context = {
        'title': '首页',
        'swiper_imgs': swiper_imgs,
        'nav_imgs': nav_imgs,
        'mustbuy_imgs': mustbuy_imgs,
    }
    return render(request, 'main/home.html', context=context)


def market(request):
    catid = request.GET.get('catid', '1')
    childclass = request.GET.get('childclass', '0')
    sortrule = request.GET.get('sortrule', '1')
    goodtypes = GoodType.objects.all()
    user = request.user

    ### 获取用户购物车数据
    carts = Cart.objects.filter(c_user=user)
    cart_goodsid = {}
    if carts.exists():
        for cart in carts:
            cart_goodsid[cart.c_good] = cart.c_goods_num

    ### 子类过滤
    # filter永远返回一个QuerySet，需要索引获取单条记录
    # subclass_str = GoodType.objects.filter(typeid=catid)[0].childtypenames
    # get返回单条记录
    subclass_str = GoodType.objects.get(typeid=catid).childtypenames
    # print(subclass_str)
    subclass_list = [item.split(':') for item in subclass_str.split('#')]
    # print(subclass_list)
    if int(childclass) == 0:
        # 0表示全部分类
        goods_list = Goods.objects.filter(categoryid=catid)
    else:
        # 否则根据子类来过滤
        goods_list = Goods.objects.filter(categoryid=catid).filter(childcid=childclass)

    ### 排序规则
    rules = [
        ['综合排序', '1'],
        ['价格升序', '2'],
        ['价格降序', '3'],
    ]
    # 没有switch/case语法确实很难
    if sortrule == '1':
        pass
    elif sortrule == '2':
        # order_by不会直接修改原数据，要重新赋值
        goods_list = goods_list.order_by('price')
    elif sortrule == '3':
        goods_list = goods_list.order_by('-price')
    # print(goods_list)
    context = {
        'title': '商城',
        'catid': int(catid),
        'goodtypes': goodtypes,
        'goods_list': goods_list,
        'subclass_list': subclass_list,
        'childcid': childclass,
        'rules': rules,
        'sortrule': sortrule,
        'cart_goodsid': cart_goodsid,
    }
    return render(request, 'main/market.html', context=context)


def cart(request):
    user = request.user
    carts = Cart.objects.filter(c_user=user)
    is_all_select = not carts.filter(c_is_selected=False).exists()
    context = {
        'title': '购物车',
        'carts': carts,
        'is_all_select': is_all_select,
        'total_price': total_price(user),
    }
    return render(request, 'main/cart.html', context=context)


def mine(request):
    username = request.session.get('username')
    context = {
        'title': '我的',
        'is_login': False,
    }
    if username:
        user = User.objects.get(Q(username=username) | Q(email=username))
        context['is_login'] = True
        context['username'] = user.username
        context['icon'] = MEDIA_ROOT_PREFIX + user.icon.url  # 记住将ImageField对象转为url
        context['order_not_pay_count'] = Order.objects.filter(o_user=user).filter(o_status=0).count()
        context['order_not_received_count'] = Order.objects.filter(o_user=user).filter(o_status=1).count()
    return render(request, 'main/mine.html', context=context)


def test(request):
    """
    给mysql商品添加随机商品价格
    """
    goods = Goods.objects.all()
    for good in goods:
        good.price = random.randint(1, 500) / 10
        good.marketprice = good.price + 2
        good.save()
    return HttpResponse('Ok!')


def register(request):
    if request.method == 'GET':
        context = {
            'title': '注册',
        }
        return render(request, 'user/register.html', context=context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        # password = request.POST.get('password')
        password = my_password_generator(request.POST.get('password'))
        icon = request.FILES.get('icon')

        user = User()
        user.username = username
        user.email = email
        user.password = password
        user.icon = icon
        user.save()
        u_token = uuid.uuid4().hex
        print(u_token)
        cache.set(u_token, username, timeout=60 * 60 * 24)
        # 暂时还不成功，需要用到celery来在后台运行，或者因为是在windows平台
        # p = Process(target=send_verification_email, args=(username, email, u_token))
        # p.start()
        send_verification_email(username, email, u_token)
        return HttpResponseRedirect(reverse('shop:login'))


def login(request):
    if request.method == 'GET':
        context = {
            'title': '登录',
        }
        login_error = request.session.get('login_error')  # 利用session存储临时前后端交互内容
        if login_error:
            del request.session['login_error']
            context['login_error'] = login_error
        return render(request, 'user/login.html', context=context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(Q(username=username) | Q(email=username))
        if users.exists():
            user = users.first()
            if my_password_checker(password, user.password):
                if user.is_active:
                    request.session['username'] = username
                    return HttpResponseRedirect(reverse('shop:mine'))
                else:
                    request.session['login_error'] = '**用户未激活**'
                    return HttpResponseRedirect(reverse('shop:login'))
            else:
                request.session['login_error'] = '**密码错误**'
                return HttpResponseRedirect(reverse('shop:login'))
        else:
            request.session['login_error'] = '**用户不存在**'
            return HttpResponseRedirect(reverse('shop:login'))


def checkuser(request):
    username = request.GET.get('username')
    users = User.objects.filter(username=username)
    if users.exists():
        data = {
            'status': 900,
            'message': '用户名已被占用'
        }
    else:
        data = {
            'status': 901,
            'message': '用户名可用'
        }
    return JsonResponse(data=data)


def checkemail(request):
    email = request.GET.get('email')
    users = User.objects.filter(email=email)
    if users.exists():
        data = {
            'status': 900,
            'message': '邮箱已被占用'
        }
    else:
        data = {
            'status': 901,
            'message': '邮箱可用'
        }
    return JsonResponse(data=data)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('shop:mine'))


def activate(request):
    u_token = request.GET.get('u_token')
    username = cache.get(u_token)
    if username:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('shop:login'))
    else:
        return HttpResponse('激活失败！')


def testchche(request):
    cache.set('name', 'xiaofu')
    return HttpResponse('测试成功')


def add_to_cart(request):
    goodsid = request.GET.get('goodsid')
    user = request.user
    carts = Cart.objects.filter(c_good__productid=goodsid).filter(c_user=user)
    data = {
        'status': 700,
        'num': 1,
    }
    if carts.exists():
        cart = carts.first()
        cart.c_goods_num = cart.c_goods_num + 1
        cart.save()
        data['num'] = cart.c_goods_num
    else:
        cart = Cart()
        cart.c_good = Goods.objects.get(productid=goodsid)
        cart.c_user = user
        cart.save()

    return JsonResponse(data)


def delete_from_cart(request):
    goodsid = request.GET.get('goodsid')
    user = request.user
    carts = Cart.objects.filter(c_good__productid=goodsid).filter(c_user=user)
    data = {
        'status': 700,
    }
    if carts.exists():
        cart = carts.first()
        cart.c_goods_num = cart.c_goods_num - 1
        if cart.c_goods_num < 0:
            cart.c_goods_num = 0
        cart.save()
        data['num'] = cart.c_goods_num
    else:
        data['num'] = 0
    return JsonResponse(data)


def change_select_state(request):
    cartid = request.GET.get('cartid')
    carts = Cart.objects.filter(pk=cartid)
    user = request.user
    data = {
        'status': 700,
    }
    if carts.exists():
        cart = carts.first()
        cart.c_is_selected = not cart.c_is_selected
        cart.save()
        data['is_selected'] = cart.c_is_selected
        is_all_select = not Cart.objects.filter(c_user=user).filter(c_is_selected=False).exists()
        data['is_all_select'] = is_all_select
        data['total_price'] = total_price(user)
    return JsonResponse(data)


def delete_in_cart(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    user = request.user
    data = {
        'status': 700,
    }
    if cart.c_goods_num > 1:
        cart.c_goods_num = cart.c_goods_num - 1
        cart.save()
        data['num'] = cart.c_goods_num
    else:
        cart.delete()
        data['num'] = 0
    data['total_price'] = total_price(user)
    return JsonResponse(data)


def add_in_cart(request):
    cartid = request.GET.get('cartid')
    user = request.user
    cart = Cart.objects.get(pk=cartid)
    cart.c_goods_num = cart.c_goods_num + 1
    cart.save()
    data = {
        'status': 700,
        'num': cart.c_goods_num,
        'total_price': total_price(user),
    }
    return JsonResponse(data)


@csrf_exempt
def testlist(request):
    names = request.POST.get('method')
    print(request.POST)
    print(names)
    return HttpResponse('ok')


def cart_all_unselect(request):
    user = request.user
    carts = Cart.objects.filter(c_user=user)
    data = {
        'status': 700,
    }
    if carts.exists():
        for cart in carts:
            cart.c_is_selected = False
            cart.save()
    return JsonResponse(data)


def cart_all_select(request):
    user = request.user
    carts = Cart.objects.filter(c_user=user)
    data = {
        'status': 700,
    }
    if carts.exists():
        for cart in carts:
            cart.c_is_selected = True
            cart.save()
    return JsonResponse(data)


def make_order(request):
    user = request.user
    carts = Cart.objects.filter(c_user=user).filter(c_is_selected=True)
    # 生成订单
    order = Order()
    order.o_user = user
    order.o_price = total_price(user)
    order.save()
    # 订单和商品级联
    for cart in carts:
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods = cart.c_good
        ordergoods.o_goods_num = cart.c_goods_num
        ordergoods.save()
        cart.delete()
    data = {
        'status': 700,
        'msg': 'ok',
        'order_id': order.id,
    }
    return JsonResponse(data)


def orderdetails(request):
    orderid = request.GET.get('order_id')
    order = Order.objects.get(pk=orderid)
    context = {
        'title': '订单详情',
        'order': order,
    }
    return render(request, 'order/order_detail.html', context=context)


def orderlist_not_pay(request):
    orders = Order.objects.filter(o_user=request.user).filter(o_status=0)
    context = {
        'title': '未付款订单',
        'orders': orders,
    }
    return render(request, 'order/orderlist_not_pay.html', context=context)


def paid(request):
    orderid = request.GET.get('order_id')
    order = Order.objects.get(pk=orderid)
    order.o_status = 1
    order.save()
    data = {
        'status': 700,
    }
    return JsonResponse(data)


def alipay(request):
    alipay = AliPay(
        appid="2016102500758026",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=open(os.path.join(BASE_DIR, 'alipay_keys/app_private_key'), 'r').read(),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=open(os.path.join(BASE_DIR, 'alipay_keys/alipay_public_key'), 'r').read(),
        sign_type="RSA",  # RSA 或者 RSA2
        debug=False,  # 默认False
        config=AliPayConfig(timeout=15)  # 可选, 请求超时时间
    )

    subject = '特斯拉Model3'

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no="20201002001",
        total_amount=10000,
        subject=subject,
        return_url="https://www.baidu.com",
        notify_url="https://www.baidu.com",  # 可选, 不填则使用默认notify url
    )

    return redirect('https://openapi.alipaydev.com/gateway.do?' + order_string)
