from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class UserData(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number=PhoneNumberField()
