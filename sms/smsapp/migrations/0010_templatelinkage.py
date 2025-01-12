# Generated by Django 5.0.6 on 2024-10-04 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0009_scheduledmessage_alter_reportinfo_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateLinkage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('template_name', models.CharField(max_length=255)),
                ('button_name', models.CharField(max_length=100)),
                ('useremail', models.CharField(max_length=100)),
                ('linked_template_name', models.CharField(max_length=100)),
            ],
        ),
    ]
