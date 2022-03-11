# Generated by Django 4.0.3 on 2022-03-07 18:27

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
                ('created', models.DateTimeField(auto_created=True, editable=False)),
                ('user_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=20)),
                ('device_token', models.CharField(max_length=200)),
                ('is_premium_user', models.BooleanField(default=False)),
                ('did_accept_to_sand_privacy_policy', models.BooleanField(default=False)),
                ('date_accepted_to_sand_privacy_policy', models.BooleanField(default=False)),
                ('fire_monitoring_is_on', models.BooleanField(default=False)),
                ('weather_monitoring_is_on', models.BooleanField(default=False)),
                ('modified', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True, editable=False)),
                ('radius', models.FloatField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('property_name', models.CharField(max_length=255)),
                ('property_address', models.CharField(max_length=255)),
                ('modified', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]