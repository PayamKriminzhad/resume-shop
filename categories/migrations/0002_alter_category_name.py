# Generated by Django 4.1.5 on 2023-02-12 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.SlugField(max_length=150, verbose_name='عنوان در URL'),
        ),
    ]