# Generated by Django 4.0.10 on 2023-04-10 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_product_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='buying_type',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
    ]
