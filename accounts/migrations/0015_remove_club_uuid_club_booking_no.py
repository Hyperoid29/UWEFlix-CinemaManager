# Generated by Django 4.1.5 on 2023-01-13 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_club_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='uuid',
        ),
        migrations.AddField(
            model_name='club',
            name='booking_no',
            field=models.CharField(default='9143A', editable=False, max_length=50),
        ),
    ]
