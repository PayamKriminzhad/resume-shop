# Generated by Django 4.1.5 on 2023-02-09 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productcomment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت'),
        ),
    ]