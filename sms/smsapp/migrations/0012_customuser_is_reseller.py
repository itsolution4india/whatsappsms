# Generated by Django 5.0.4 on 2024-04-29 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0011_reselleruser_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_reseller',
            field=models.BooleanField(default=False),
        ),
    ]