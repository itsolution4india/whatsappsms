# Generated by Django 5.0.6 on 2024-05-15 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0032_alter_reportinfo_original_filename_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='coins',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reportinfo',
            name='original_filename',
            field=models.CharField(default='2024-05-15-09-36-02', max_length=255),
        ),
    ]
