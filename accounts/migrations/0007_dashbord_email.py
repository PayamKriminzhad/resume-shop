# Generated by Django 4.1.5 on 2023-02-06 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_dashbord_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashbord',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='ایمیل'),
        ),
    ]