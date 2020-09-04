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

class GoodType(models.Model):
    typeid=models.IntegerField(default=1)
    typename=models.CharField(max_length=32)
    childtypenames=models.CharField(max_length=255)
    typesort=models.IntegerField(default=1)
    class Meta:
        db_table='GoodType'

class Goods(models.Model):
    """
    productid,productimg,productname,productlongname,isxf,pmdesc,
    specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum
    """
    productid = models.BigIntegerField(default=1)
    productimg = models.CharField(max_length=255)
    productname = models.CharField(max_length=128)
    productlongname = models.CharField(max_length=255)
    isxf=models.BooleanField(default=0)
    pmdesc=models.CharField(max_length=64)
    specifics=models.IntegerField(default=0)
    price=models.FloatField(default=0)
    marketprice=models.FloatField(default=0)
    categoryid=models.IntegerField(default=1)
    childcid=models.IntegerField(default=1)
    childcidname=models.CharField(max_length=128)
    dealerid=models.IntegerField(default=1)
    storenums=models.IntegerField(default=1)
    productnum=models.IntegerField(default=1)

    class Meta:
        db_table='Goods'
