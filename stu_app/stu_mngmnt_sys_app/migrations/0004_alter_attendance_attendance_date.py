# Generated by Django 4.1.1 on 2022-10-01 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu_mngmnt_sys_app', '0003_leavereportstaff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(),
        ),
    ]
