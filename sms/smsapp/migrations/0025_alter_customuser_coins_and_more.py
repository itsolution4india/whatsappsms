# Generated by Django 5.0.4 on 2024-05-09 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0024_alter_reportinfo_original_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='coins',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reportinfo',
            name='original_filename',
            field=models.CharField(default='2024-05-09-09-37-41', max_length=255),
        ),
    ]
