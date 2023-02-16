# Generated by Django 4.1.5 on 2023-01-30 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamics', '0002_sitesetting_facebook_sitesetting_home_sentence_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='skype',
            field=models.CharField(default=0, max_length=50, verbose_name='اسکایپ'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='facebook',
            field=models.CharField(max_length=50, verbose_name='فیس بوک'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='instagram',
            field=models.CharField(max_length=50, verbose_name='اینستاگرام'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='tweeter',
            field=models.CharField(max_length=50, verbose_name='توییتر'),
        ),
    ]
