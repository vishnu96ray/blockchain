# Generated by Django 3.1.7 on 2021-05-18 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_holidays'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_approved',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
