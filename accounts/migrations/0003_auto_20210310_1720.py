# Generated by Django 3.1 on 2021-03-10 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210310_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='receipt_pic',
            field=models.FileField(blank=True, null=True, upload_to='uploads/recepts'),
        ),
    ]
