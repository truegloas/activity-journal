# Generated by Django 3.2.4 on 2021-06-12 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0003_auto_20210612_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadmeasurementtype',
            name='name',
            field=models.CharField(default='Тип нагрузки', max_length=255),
        ),
    ]
