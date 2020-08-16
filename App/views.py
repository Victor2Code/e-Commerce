from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from App.models import Test


# def test(request):
#     img = Test.objects.filter(name='test1')
#     context = {
#         'img': img
#     }
#     return render(request, 'test.html', context=context)


def home(request):
    return render(request, 'main/home.html')


def market(request):
    return render(request, 'main/market.html')


def cart(request):
    return render(request, 'main/cart.html')


def mine(request):
    return render(request, 'main/mine.html')
