# Generated by Django 5.0.6 on 2024-05-16 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0033_alter_customuser_coins_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Discount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reportinfo',
            name='original_filename',
            field=models.CharField(default='2024-05-16-06-23-54', max_length=255),
        ),
    ]
