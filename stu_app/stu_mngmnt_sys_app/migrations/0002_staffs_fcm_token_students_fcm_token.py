# Generated by Django 4.1.1 on 2022-10-05 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu_mngmnt_sys_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='fcm_token',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='students',
            name='fcm_token',
            field=models.TextField(default=''),
        ),
    ]
