# Generated by Django 4.0.10 on 2023-04-17 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_customer_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='lang',
            field=models.CharField(choices=[('en', 'en'), ('ru', 'ru'), ('uz', 'uz')], default='uz', max_length=5, verbose_name='Язык'),
        ),
    ]
