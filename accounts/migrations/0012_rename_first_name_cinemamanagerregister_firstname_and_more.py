# Generated by Django 4.1.5 on 2023-01-08 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_rename_username_cinemamanagerregister_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cinemamanagerregister',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='cinemamanagerregister',
            old_name='last_name',
            new_name='lastname',
        ),
    ]
