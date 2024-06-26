# Generated by Django 5.0.6 on 2024-05-16 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0036_alter_reportinfo_original_filename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaigndata',
            name='image',
        ),
        migrations.RemoveField(
            model_name='campaigndata',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='campaigndata',
            name='text',
        ),
        migrations.RemoveField(
            model_name='campaigndata',
            name='video',
        ),
        migrations.RemoveField(
            model_name='campaigndata',
            name='voice',
        ),
        migrations.AddField(
            model_name='campaigndata',
            name='media_type',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reportinfo',
            name='original_filename',
            field=models.CharField(default='2024-05-16-09-34-41', max_length=255),
        ),
    ]
