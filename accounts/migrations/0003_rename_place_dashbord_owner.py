# Generated by Django 4.1.5 on 2023-02-03 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_dashbords_dashbord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dashbord',
            old_name='place',
            new_name='owner',
        ),
    ]