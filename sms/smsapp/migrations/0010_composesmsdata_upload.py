# Generated by Django 5.0.4 on 2024-04-26 06:27

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0009_messagesendinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComposeSmsData',
            fields=[
                ('template_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('Authencation', 'Authencation'), ('Marketing', 'Marketing'), ('Utility', 'Utility')], max_length=15)),
                ('template_data', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('approve', 'Approve'), ('pending', 'Pending')], max_length=10)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voice_message', models.FileField(blank=True, null=True, upload_to='uploads/voice_messages/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg']), django.core.validators.MaxValueValidator(5242880)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), django.core.validators.MaxValueValidator(3145728)])),
                ('pdf', models.FileField(blank=True, null=True, upload_to='uploads/pdfs/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), django.core.validators.MaxValueValidator(5242880)])),
                ('video', models.FileField(blank=True, null=True, upload_to='uploads/videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv']), django.core.validators.MaxValueValidator(5242880)])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
