from typing import Any
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, username: str, password: str = None, **extra_fields: Any) -> 'CustomUser':
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, email: str, username: str, password: str = None, **extra_fields: Any) -> 'CustomUser':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

def validate_digits(value: int, min_digits: int, max_digits: int):
    num_digits = len(str(value))
    if num_digits < min_digits:
        raise ValidationError(f'{value} has fewer than {min_digits} digits.')
    if num_digits > max_digits:
        raise ValidationError(f'{value} has more than {max_digits} digits.')

def validate_phone_number_id(value: str):
    if not value.isdigit() or len(value) != 15:
        raise ValidationError(f'{value} must be exactly 15 digits long.')

def validate_whatsapp_business_account_id(value: str):
    if not value.isdigit() or len(value) != 15:
        raise ValidationError(f'{value} must be exactly 15 digits long.')

class RegisterApp(models.Model):
    app_name = models.CharField(max_length=20)
    token = models.TextField()
    app_id = models.CharField(max_length=50)

    def __str__(self):
        return self.app_name

    def get_token(self):
        return self.token
    
    def get_app_id(self):
        return self.app_id

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number_id = models.CharField(max_length=15, default=0, validators=[validate_phone_number_id])
    whatsapp_business_account_id = models.CharField(max_length=15,default=0, validators=[validate_whatsapp_business_account_id])
    coins = models.IntegerField(default=0)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    register_app = models.ForeignKey(RegisterApp, on_delete=models.SET_NULL, null=True)
    def save(self, *args, **kwargs):
        if self.register_app:
            # Set token and app_id from RegisterApp
            self.token = self.register_app.token
            self.app_id = self.register_app.app_id
        super(CustomUser, self).save(*args, **kwargs)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email



class Whitelist_Blacklist(models.Model):
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    whitelist_phone = models.TextField()
    blacklist_phone = models.TextField()
    objects = CustomUserManager()



class ReportInfo(models.Model):
    
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campaign_title=models.CharField(max_length=50)
    contact_list= models.TextField()
    message_date = models.DateField()
    template_name=models.CharField(max_length=100)
    message_delivery = models.IntegerField()
    


class Templates(models.Model):
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    templates=models.CharField(unique=True,max_length=100)
    
