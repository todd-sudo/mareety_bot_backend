# Generated by Django 4.0.10 on 2023-04-16 11:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_customer_create_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_order',
            field=models.BooleanField(default=False, verbose_name='В заказе'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='create_at',
            field=models.DateField(default=datetime.date(2023, 4, 16), verbose_name='Дата создания'),
        ),
    ]
