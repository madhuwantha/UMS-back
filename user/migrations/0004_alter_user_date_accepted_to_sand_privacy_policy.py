# Generated by Django 4.0.3 on 2022-03-09 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_notification_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_accepted_to_sand_privacy_policy',
            field=models.DateTimeField(),
        ),
    ]