# Generated by Django 4.0.3 on 2022-03-12 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_user_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='custom_id',
            field=models.CharField(default='', max_length=30),
        ),
    ]
