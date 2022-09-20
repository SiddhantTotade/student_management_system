# Generated by Django 4.1.1 on 2022-09-20 09:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu_mngmnt_sys_app', '0004_alter_students_session_end_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='session_end_year',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='session_start_year',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]