# Generated by Django 5.0.6 on 2024-05-21 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0040_campaigndata_campaign_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportfile',
            name='original_filename',
            field=models.CharField(default='2024-05-21-05-01-46', max_length=255),
        ),
    ]
