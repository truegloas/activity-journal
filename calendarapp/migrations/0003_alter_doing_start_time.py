# Generated by Django 3.2.4 on 2021-06-09 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0002_alter_doing_doing_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doing',
            name='start_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
