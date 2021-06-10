# Generated by Django 3.2.4 on 2021-06-10 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Doing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Деятельность', max_length=255)),
                ('start_time', models.DateField(blank=True, null=True)),
                ('end_time', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DoingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Вид деятельности', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realized_load', models.DecimalField(decimal_places=2, max_digits=5)),
                ('target_load', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='LoadMeasurementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarApp',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='calendarapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='RealizeStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Шаг', max_length=255)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('doing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.doing')),
                ('load', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.load')),
            ],
        ),
        migrations.AddField(
            model_name='load',
            name='load_measurement_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.loadmeasurementtype'),
        ),
        migrations.AddField(
            model_name='doing',
            name='doing_type',
            field=models.ForeignKey(auto_created=True, blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.doingtype'),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='Текст заметки', max_length=63999)),
                ('image', models.ImageField(blank=True, default=None, upload_to='images')),
                ('doing', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.doing')),
                ('realize_step', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.realizestep')),
                ('calendar_app', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.calendarapp')),
            ],
        ),
        migrations.AddField(
            model_name='doing',
            name='calendar_app',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendarapp.calendarapp'),
        ),
    ]
