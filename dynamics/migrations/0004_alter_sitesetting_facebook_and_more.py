# Generated by Django 4.1.5 on 2023-01-30 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamics', '0003_sitesetting_skype_alter_sitesetting_facebook_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetting',
            name='facebook',
            field=models.CharField(max_length=250, verbose_name='فیس بوک'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='instagram',
            field=models.CharField(max_length=250, verbose_name='اینستاگرام'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='skype',
            field=models.CharField(max_length=250, verbose_name='اسکایپ'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='tweeter',
            field=models.CharField(max_length=250, verbose_name='توییتر'),
        ),
    ]
