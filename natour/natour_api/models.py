from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        validators=[MinLengthValidator(3)]
    )
    email = models.EmailField(unique=True, null=False, blank=False)
    cpf = models.CharField(
        max_length=11,
        null=False,
        blank=False,
        unique=True,
        validators=[MinLengthValidator(11)]
    )
    date_of_birth = models.DateField(null=False, blank=False)
    phone_number = models.CharField(
        max_length=15,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex=r'^\+55\d{2}(?:9\d{8}|\d{8})$', message="O número de telefone deve estar no formato '+55DDXXXXXXXXX' ou '+55DDXXXXXXXX'.")
        ]
    )
    password = models.CharField(
        max_length=128,  # Default max length for Django hashed passwords
        null=False,
        blank=False
    )
    photo = models.ImageField(upload_to='Images/', blank=True, null=True, default='Images/doc.jpg')
    ROLE_CHOICES = [
        ('master', 'Master'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'cpf', 'date_of_birth', 'phone_number']

    def get_natural_key(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:  # New user creation
            self.password = make_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-createdAt']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
