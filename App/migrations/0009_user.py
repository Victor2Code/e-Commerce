# Generated by Django 3.0.3 on 2020-09-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_auto_20200904_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('email', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('icon', models.ImageField(upload_to='icons/%Y/%m/%d/')),
                ('is_active', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
