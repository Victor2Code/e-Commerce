from django.db import models


# Create your models here.

# class Test(models.Model):
#     name = models.CharField(max_length=16)
#     location = models.CharField(max_length=255)

class Main(models.Model):
    img = models.CharField(max_length=255)  # 图片地址
    name = models.CharField(max_length=64)  # 图片名称
    trackid = models.IntegerField(default=1)  # 图片id
    class Meta:
        abstract = True


class MainSwiper(Main):
    class Meta:
        db_table = 'MainSwiper'

class MainNav(Main):
    class Meta:
        db_table = 'MainNav'

class MainMustBuy(Main):
    class Meta:
        db_table = 'MainMustBuy'
