# Generated by Django 4.0.10 on 2023-04-09 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_customer_tg_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Изображение'),
        ),
    ]
