# Generated by Django 3.0.3 on 2020-09-04 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_goods'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='productid',
            field=models.BigIntegerField(default=1),
        ),
    ]
