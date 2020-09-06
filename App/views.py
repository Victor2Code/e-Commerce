import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# from App.models import Test


# def test(request):
#     img = Test.objects.filter(name='test1')
#     context = {
#         'img': img
#     }
#     return render(request, 'test.html', context=context)
from App.models import MainSwiper, MainNav, MainMustBuy, GoodType, Goods


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
    }
    return render(request, 'main/market.html', context=context)


def cart(request):
    return render(request, 'main/cart.html')


def mine(request):
    return render(request, 'main/mine.html')


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
